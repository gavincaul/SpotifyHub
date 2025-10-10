from flask import Flask, jsonify, request
from .utils.errors import APIError
import os
from flask_cors import CORS
from .functions.commands.playlistCommands import PlaylistCommands
from .functions.spotifymanager import SpotifyManager
from .functions.commands.albumCommands import AlbumCommands
from .functions.commands.artistCommands import ArtistCommands
from .functions.commands.currentuserCommands import CurrentUserCommands
from .functions.commands.searchCommands import SearchCommands
from .functions.commands.songCommands import SongCommands
from .functions.commands.userCommands import UserCommands

# routes
from .functions.routes.playlistRoutes import playlist_bp
from .functions.routes.albumRoutes import album_bp
from .functions.routes.artistRoutes import artist_bp
from .functions.routes.currentUserRoutes import currentuser_bp
from .functions.routes.searchRoutes import search_bp
from .functions.routes.songRoutes import song_bp
from .functions.routes.userRoutes import user_bp

def create_app():

    app = Flask(__name__)
    CORS(app, origins="http://localhost:3000", supports_credentials=True,   methods=["GET", "POST", "OPTIONS", "PUT", "DELETE"],)

    @app.errorhandler(APIError)
    def handle_api_error(error):
        response = jsonify(error.to_dict())
        response.status_code = error.status_code
        return response

    # ✅ Catch unhandled exceptions (fallback)

    @app.errorhandler(Exception)
    def handle_unexpected_error(error):
        is_dev = os.getenv("FLASK_ENV") == "development"
        response = {"error": "Internal Server Error"}
        if is_dev:
            response["details"] = str(error)
        return jsonify(response), 500

    # single SpotifyManager instance
    spotify_manager = SpotifyManager()

    # commands layer (shared across routes)
    playlist_commands = PlaylistCommands(spotify_manager)
    album_commands = AlbumCommands(spotify_manager)
    artist_commands = ArtistCommands(spotify_manager)
    currentuser_commands = CurrentUserCommands(spotify_manager)
    search_commands = SearchCommands(spotify_manager)
    song_commands = SongCommands(spotify_manager)
    user_commands = UserCommands(spotify_manager)

    # attach commands to app so routes can grab them
    app.config["spotify_manager"] = spotify_manager
    app.config["playlist_commands"] = playlist_commands
    app.config["album_commands"] = album_commands
    app.config["artist_commands"] = artist_commands
    app.config["currentuser_commands"] = currentuser_commands
    app.config["search_commands"] = search_commands
    app.config["song_commands"] = song_commands
    app.config["user_commands"] = user_commands

    # register blueprints
    app.register_blueprint(playlist_bp, url_prefix="/playlist")
    app.register_blueprint(album_bp, url_prefix="/album")
    app.register_blueprint(artist_bp, url_prefix="/artist")
    app.register_blueprint(currentuser_bp, url_prefix="/me")
    app.register_blueprint(search_bp, url_prefix="/search")
    app.register_blueprint(song_bp, url_prefix="/song")
    app.register_blueprint(user_bp, url_prefix="/user")

    return app
