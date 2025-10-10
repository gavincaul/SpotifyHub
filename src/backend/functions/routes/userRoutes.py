from flask import Blueprint, jsonify, current_app, request
from .currentUserRoutes import check_logged_in
from ...utils.errors import *

user_bp = Blueprint("user", __name__)


@user_bp.route("/get/<user_id>", methods=["GET"])
def get_song(user_id):
    try:
        raw_data = request.args.get("raw", "false").lower() == "true"
        user_commands = current_app.config["user_commands"]
        return jsonify(user_commands.get_user_info(user_id, raw_data))
    except SpotifyException as e:
        raise map_spotify_error(e, "user", user_id)
    except Exception as e:
        raise TrackOperationError(
            f"Unexpected error retrieving track: {str(e)}")


@user_bp.route("/check_exists/<user_id>", methods=["GET"])
def check_exists(user_id):
    try:
        user_commands = current_app.config["user_commands"]
        return jsonify({"exists": user_commands.check_exists(user_id)})
    except SpotifyException as e:
        raise map_spotify_error(e, "user", user_id)
    except Exception as e:
        raise TrackOperationError(
            f"Unexpected error retrieving track: {str(e)}")

@user_bp.route("/playlists/<user_id>", methods=["GET"])
def user_playlists(user_id):
    try:
        user_commands = current_app.config["user_commands"]
        return jsonify(user_commands.get_user_playlists(user_id))
    except SpotifyException as e:
        raise map_spotify_error(e, "user", user_id)
    except Exception as e:
        raise TrackOperationError(
            f"Unexpected error retrieving track: {str(e)}")
