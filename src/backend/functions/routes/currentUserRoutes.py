from flask import Blueprint, request, jsonify, current_app
from ...utils.errors import *
from ..models.currentuser import CurrentUser
import spotipy
currentuser_bp = Blueprint("currentuser", __name__)
import time

def check_logged_in(error=CurrentUserOperationError):
    currentuser_cmds = current_app.config.get("currentuser_commands")
    if not currentuser_cmds:
        raise error("No user commands available")
    # Attempt to restore current_user if missing
    if not currentuser_cmds.current_user:
        if not currentuser_cmds._get_or_restore_current_user():
            raise UnauthorizedError("User not logged in")


@currentuser_bp.route("/login/start", methods=["GET"])
def login_start():
    try:
        spotify_manager = current_app.config["spotify_manager"]
        auth_url = spotify_manager.get_auth_url()
        
        return jsonify({"auth_url": auth_url})
    except SpotifyException as e:
        raise map_spotify_error(e, "current_user", "self")
    except Exception as e:
        raise CurrentUserOperationError(f"Unexpected error starting login: {str(e)}")


@currentuser_bp.route("/login/callback", methods=["GET"])
def login_callback():
    try:
        spotify_manager = current_app.config["spotify_manager"]
        code = request.args.get("code")
        currentuser_cmds = current_app.config.get("currentuser_commands")

        if not code:
            raise BadRequestError("Missing authorization code")
        
        # This does the complete flow:
        # 1. Exchanges code for tokens
        # 2. Gets user info from Spotify  
        # 3. Caches tokens with user-specific Redis key
        # 4. Sets up authenticated client
        spotify_user_id = spotify_manager.login_with_code(code)
        
        # Now you have the actual Spotify user ID
        currentuser_cmds.current_user = CurrentUser(spotify_manager=spotify_manager)
        user_data = currentuser_cmds.get_profile()

        return jsonify({
            "message": f"Logged in as {spotify_user_id}",
            "user_id": spotify_user_id,  # This is the actual Spotify user ID
            "user_data": user_data
        })
    except SpotifyException as e:
        raise map_spotify_error(e, "current_user", "self")
    except Exception as e:
        raise CurrentUserOperationError(f"Unexpected error in callback: {str(e)}")


@currentuser_bp.route("/logout", methods=["POST"])
def logout():
    try:
        check_logged_in()

        currentuser_cmds = current_app.config.get("currentuser_commands")
        currentuser_cmds.logout()  # Reset current user to force reload
        return jsonify({"code": 200, "message": "User logged out successfully"})
    except SpotifyException as e:
        raise map_spotify_error(e, "current_user", "self")
    except Exception as e:
        raise CurrentUserOperationError(
            f"Unexpected error logging out: {str(e)}")


@currentuser_bp.route("/get", methods=["GET"])
def get_user_profile():
    try:
        check_logged_in()
        currentuser_cmds = current_app.config.get("currentuser_commands")
        raw_data = request.args.get("raw", "false").lower() == "true"
        user_data = currentuser_cmds.get_profile(raw=raw_data)
        return jsonify(user_data)
    except SpotifyException as e:
        raise map_spotify_error(e, "current_user", "self")
    except Exception as e:
        raise CurrentUserOperationError(
            f"Unexpected error fetching profile: {str(e)}")


@currentuser_bp.route("/top/tracks", methods=["GET"])
def get_user_top_tracks():
    try:
        check_logged_in()
        currentuser_cmds = current_app.config.get("currentuser_commands")
        count = request.args.get("count", 10)
        time_range = request.args.get("time_range", "medium_term")
        top_tracks = currentuser_cmds.get_top_tracks(
            time_range=time_range, limit=int(count))
        return jsonify(top_tracks)
    except SpotifyException as e:
        raise map_spotify_error(e, "current_user", "self")
    except Exception as e:
        raise CurrentUserOperationError(
            f"Unexpected error fetching top tracks: {str(e)}")


@currentuser_bp.route("/top/artists", methods=["GET"])
def get_user_top_artists():
    try:
        check_logged_in()
        currentuser_cmds = current_app.config.get("currentuser_commands")
        count = request.args.get("count", 10)
        time_range = request.args.get("time_range", "medium_term")
        top_tracks = currentuser_cmds.get_top_artists(
            time_range=time_range, limit=int(count))
        return jsonify(top_tracks)
    except SpotifyException as e:
        raise map_spotify_error(e, "current_user", "self")
    except Exception as e:
        raise CurrentUserOperationError(
            f"Unexpected error fetching top artists: {str(e)}")


@currentuser_bp.route("/unfollow/user/<user_id>", methods=["DELETE"])
def unfollow_user(user_id):

    try:
        check_logged_in()
        currentuser_cmds = current_app.config.get("currentuser_commands")
        currentuser_cmds.unfollow_user(user_id)
        return jsonify({"message": f"Unfollowed user {user_id}"})
    except SpotifyException as e:
        raise map_spotify_error(e, "current_user", "self")
    except Exception as e:
        raise CurrentUserOperationError(
            f"Unexpected error unfollowing user: {str(e)}")


@currentuser_bp.route("/follow/user/<user_id>", methods=["PUT"])
def follow_user(user_id):

    try:
        check_logged_in()
        currentuser_cmds = current_app.config.get("currentuser_commands")
        currentuser_cmds.follow_user(user_id)
        return jsonify({"message": f"Followed user {user_id}"})
    except SpotifyException as e:
        raise map_spotify_error(e, "current_user", "self")
    except Exception as e:
        raise CurrentUserOperationError(
            f"Unexpected error following user: {str(e)}")


@currentuser_bp.route("/unfollow/artist/<artist_id>", methods=["DELETE"])
def unfollow_artist(artist_id):

    try:
        check_logged_in()
        currentuser_cmds = current_app.config.get("currentuser_commands")
        currentuser_cmds.unfollow_artist(artist_id)
        return jsonify({"message": f"Unfollowed artist {artist_id}"})
    except SpotifyException as e:
        raise map_spotify_error(e, "current_user", "self")
    except Exception as e:
        raise CurrentUserOperationError(
            f"Unexpected error unfollowing artist: {str(e)}")


@currentuser_bp.route("/follow/artist/<artist_id>", methods=["PUT"])
def follow_artist(artist_id):

    try:
        check_logged_in()
        currentuser_cmds = current_app.config.get("currentuser_commands")
        currentuser_cmds.follow_artist(artist_id)
        return jsonify({"message": f"Followed artist {artist_id}"})
    except SpotifyException as e:
        raise map_spotify_error(e, "current_user", "self")
    except Exception as e:
        raise CurrentUserOperationError(
            f"Unexpected error following artist: {str(e)}")


@currentuser_bp.route("/unfollow/playlist/<playlist_id>", methods=["DELETE"])
def unfollow_playlist(playlist_id):

    try:
        check_logged_in()
        currentuser_cmds = current_app.config.get("currentuser_commands")
        currentuser_cmds.unfollow_playlist(playlist_id)
        return jsonify({"message": f"Unfollowed playlist {playlist_id}"})
    except SpotifyException as e:
        raise map_spotify_error(e, "current_user", "self")
    except Exception as e:
        raise CurrentUserOperationError(
            f"Unexpected error unfollowing playlist: {str(e)}")


@currentuser_bp.route("/follow/playlist/<playlist_id>", methods=["PUT"])
def follow_playlist(playlist_id):
    try:
        check_logged_in()
        currentuser_cmds = current_app.config.get("currentuser_commands")
        currentuser_cmds.follow_playlist(playlist_id)
        return jsonify({"message": f"Followed playlist {playlist_id}"})
    except SpotifyException as e:
        raise map_spotify_error(e, "current_user", "self")
    except Exception as e:
        raise CurrentUserOperationError(
            f"Unexpected error following playlist: {str(e)}")


@currentuser_bp.route("/delete/track/<track_id>", methods=["DELETE"])
def delete_saved_tracks(track_id):
    try:
        check_logged_in()
        currentuser_cmds = current_app.config.get("currentuser_commands")
        currentuser_cmds.delete_saved_tracks(track_id)
        return jsonify({"message": f"Deleted saved track(s)"})
    except SpotifyException as e:
        raise map_spotify_error(e, "current_user", "self")
    except Exception as e:
        raise CurrentUserOperationError(
            f"Unexpected error deleting saved track: {str(e)}")


@currentuser_bp.route("/save/track/<track_id>", methods=["PUT"])
def save_tracks(track_id):
    try:
        check_logged_in()
        currentuser_cmds = current_app.config.get("currentuser_commands")
        currentuser_cmds.save_tracks(track_id)
        return jsonify({"message": f"Saved track(s)"})
    except SpotifyException as e:
        raise map_spotify_error(e, "current_user", "self")
    except Exception as e:
        raise CurrentUserOperationError(
            f"Unexpected error saving track: {str(e)}")


@currentuser_bp.route("/delete/album/<album_id>", methods=["DELETE"])
def delete_saved_albums(album_id):
    try:
        check_logged_in()
        currentuser_cmds = current_app.config.get("currentuser_commands")
        currentuser_cmds.delete_saved_albums(album_id)
        return jsonify({"message": f"Deleted saved album(s)"})
    except SpotifyException as e:
        raise map_spotify_error(e, "current_user", "self")
    except Exception as e:
        raise CurrentUserOperationError(
            f"Unexpected error deleting saved album: {str(e)}")


@currentuser_bp.route("/save/album/<album_id>", methods=["PUT"])
def save_albums(album_id):
    try:
        check_logged_in()
        currentuser_cmds = current_app.config.get("currentuser_commands")
        currentuser_cmds.save_albums(album_id)
        return jsonify({"message": f"Saved album(s)"})
    except SpotifyException as e:
        raise map_spotify_error(e, "current_user", "self")
    except Exception as e:
        raise CurrentUserOperationError(
            f"Unexpected error saving album: {str(e)}")


@currentuser_bp.route("/create/playlist", methods=["POST"])
def create_playlist():
    try:
        check_logged_in()
        currentuser_cmds = current_app.config.get("currentuser_commands")
        data = request.args
        name = data.get("name", "New Playlist")
        description = data.get("description", "")
        public = data.get("public", True)
        collaborative = data.get("collaborative", False)
        playlist_id = currentuser_cmds.create_playlist(
            name, description, public, collaborative)
        return jsonify({"message": f"Created playlist {name}", "playlist_id": playlist_id})
    except SpotifyException as e:
        raise map_spotify_error(e, "current_user", "self")
    except Exception as e:
        raise CurrentUserOperationError(
            f"Unexpected error creating playlist: {str(e)}")


@currentuser_bp.route("/delete/playlist/<playlist_id>", methods=["DELETE"])
def delete_playlist(playlist_id):
    try:
        check_logged_in()
        currentuser_cmds = current_app.config.get("currentuser_commands")
        currentuser_cmds.delete_playlist(playlist_id)
        return jsonify({"message": f"Deleted playlist {playlist_id}"})
    except SpotifyException as e:
        raise map_spotify_error(e, "current_user", "self")
    except Exception as e:
        raise CurrentUserOperationError(
            f"Unexpected error deleting playlist: {str(e)}")


@currentuser_bp.route("/devices", methods=["GET"])
def get_user_devices():
    try:
        check_logged_in()
        currentuser_cmds = current_app.config.get("currentuser_commands")
        devices = currentuser_cmds.get_devices()
        return jsonify(devices)
    except SpotifyException as e:
        raise map_spotify_error(e, "current_user", "self")
    except Exception as e:
        raise CurrentUserOperationError(
            f"Unexpected error fetching devices: {str(e)}")


@currentuser_bp.route("/playlists", methods=["GET"])
def get_user_playlists():
    try: 
        check_logged_in()
        currentuser_cmds = current_app.config.get("currentuser_commands")
        playlists = currentuser_cmds.get_playlists()
        return jsonify(playlists)
    except SpotifyException as e:
        raise map_spotify_error(e, "current_user", "self")
    except Exception as e:
        raise CurrentUserOperationError(
            f"Unexpected error fetching playlists: {str(e)}")


@currentuser_bp.route("/albums", methods=["GET"])
def get_user_albums():
    check_logged_in()
    try:
        currentuser_cmds = current_app.config.get("currentuser_commands")
        albums = currentuser_cmds.get_albums()
        return jsonify(albums)
    except SpotifyException as e:
        raise map_spotify_error(e, "current_user", "self")
    except Exception as e:
        raise CurrentUserOperationError(
            f"Unexpected error fetching albums: {str(e)}")

@currentuser_bp.route("/tracks", methods=["GET"])
def get_user_tracks():
    check_logged_in()
    try:
        currentuser_cmds = current_app.config.get("currentuser_commands")
        tracks = currentuser_cmds.get_tracks()
        return jsonify(tracks)
    except SpotifyException as e:
        raise map_spotify_error(e, "current_user", "self")
    except Exception as e:
        raise CurrentUserOperationError(
            f"Unexpected error fetching tracks: {str(e)}")

@currentuser_bp.route("/artists", methods=["GET"])
def get_user_artists():
    check_logged_in()
    try:
        currentuser_cmds = current_app.config.get("currentuser_commands")
        artists = currentuser_cmds.get_artists()
        return jsonify(artists)
    except SpotifyException as e:
        raise map_spotify_error(e, "current_user", "self")
    except Exception as e:
        raise CurrentUserOperationError(
            f"Unexpected error fetching artists: {str(e)}")


@currentuser_bp.route("/library", methods=["GET"])
def get_user_library():
    check_logged_in()
    try:
        currentuser_cmds = current_app.config.get("currentuser_commands")
        library = currentuser_cmds.get_library()
        return jsonify(library)
    except SpotifyException as e:
        raise map_spotify_error(e, "current_user", "self")
    except Exception as e:
        raise CurrentUserOperationError(
            f"Unexpected error fetching library: {str(e)}")