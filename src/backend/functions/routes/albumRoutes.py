from flask import Blueprint, request, jsonify, current_app
from ...utils.errors import *
album_bp = Blueprint("album", __name__)


@album_bp.route("/get/<album_id>", methods=["GET"])
def get_album(album_id):
    try:
        ac = current_app.config.get("album_commands")  # album commands
        raw_data = request.args.get("raw", "false").lower() == "true"
        album = ac.check_album(album_id)
        if raw_data:
            return jsonify(album.get_album())
        data = album.get_album_info()
        return jsonify(data)
    except SpotifyException as e:
        raise map_spotify_error(e, "album", album_id)
    except Exception as e:
        raise AlbumOperationError(
            f"Unexpected error retrieving album: {str(e)}")


@album_bp.route("/get_tracks/<album_id>", methods=["GET"])
def get_album_tracks(album_id):
    ac = current_app.config.get("album_commands")  # album commands
    try:
        positions = request.args.get("positions", "false").lower() == "true"
        return ac.get_album_track_list(album_id, positions=positions)

    except NotFoundError as e:
        raise e
    except Exception as e:
        raise SpotifyAPIError(f"Error retrieving album: {str(e)}")


@album_bp.route("/check_exists/<album_id>", methods=["GET"])
def check_album_exists(album_id):
    ac = current_app.config.get("album_commands")  # album commands
    try:
        return jsonify({"exists": ac.check_exists(album_id)})

    except NotFoundError as e:
        raise e
    except Exception as e:
        raise SpotifyAPIError(f"Error retrieving album: {str(e)}")


@album_bp.route("/artists/<album_id>", methods=["GET"])
def get_album_artists(album_id):
    ac = current_app.config.get("album_commands")  # album commands
    try:
        artists = ac.get_album_artists(album_id)
        return jsonify({"artists": artists})

    except NotFoundError as e:
        raise e
    except Exception as e:
        raise SpotifyAPIError(f"Error retrieving album: {str(e)}")
