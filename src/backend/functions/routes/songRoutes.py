from flask import Blueprint, jsonify, current_app, request
from .currentUserRoutes import check_logged_in
from ...utils.errors import *
song_bp = Blueprint("song", __name__)


@song_bp.route("/get/<song_id>", methods=["GET"])
def get_song(song_id):
    try:
        raw_data = request.args.get("raw", "false").lower() == "true"
        song_commands = current_app.config["song_commands"]
        return jsonify(song_commands.get_song_info(song_id, raw_data))
    except SpotifyException as e:
        raise map_spotify_error(e, "song", song_id)
    except Exception as e:
        raise TrackOperationError(
            f"Unexpected error retrieving track: {str(e)}")


@song_bp.route("/check_exists/<song_id>", methods=["GET"])
def check_exists(song_id):
    try:
        song_commands = current_app.config["song_commands"]
        return jsonify({"exists": song_commands.check_exists(song_id)})
    except SpotifyException as e:
        raise map_spotify_error(e, "song", song_id)
    except Exception as e:
        raise TrackOperationError(
            f"Unexpected error retrieving track: {str(e)}")


@song_bp.route("/check_playlist/<song_id>/<playlist_id>", methods=["GET"])
def check_song_on_playlist(song_id, playlist_id):
    try:
        playlist_commands = current_app.config["playlist_commands"]

        playlist = playlist_commands.check_playlist(playlist_id)
        track_ids = playlist.get_playlist_track_ids(
            total=playlist.get_playlist_length())

        return jsonify({"exists": song_id in track_ids, "playlist_id": playlist_id}), 200

    except SpotifyException as e:
        raise map_spotify_error(e, "song", song_id)
    except Exception as e:
        raise TrackOperationError(
            f"Unexpected error checking song on playlist: {str(e)}"
        )
