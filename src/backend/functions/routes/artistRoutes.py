from flask import Blueprint, request, jsonify, current_app
from ...utils.errors import *
artist_bp = Blueprint("artist", __name__)


@artist_bp.route("/get/<artist_id>", methods=["GET"])
def get_artist(artist_id):
    try:
        ac = current_app.config.get("artist_commands")  # album commands
        raw_data = request.args.get("raw", "false").lower() == "true"
        artist = ac.check_artist(artist_id)
        if raw_data:
            return jsonify(artist.get_artist())
        data = artist.get_artist_info()
        return jsonify(data)
    except SpotifyException as e:
        raise map_spotify_error(e, "artist", artist_id)
    except Exception as e:
        raise ArtistOperationError(
            f"Unexpected error retrieving artist: {str(e)}")


@artist_bp.route("/check_exists/<artist_id>", methods=["GET"])
def check_artist_exists(artist_id):
    ac = current_app.config.get("artist_commands")  # album commands
    try:
        return jsonify({"exists": ac.check_exists(artist_id)})

    except NotFoundError as e:
        raise e
    except Exception as e:
        raise SpotifyAPIError(f"Error retrieving album: {str(e)}")


@artist_bp.route("/top_tracks/<artist_id>", methods=["GET"])
def get_artist_top_tracks(artist_id):
    raw_data = request.args.get("raw", "false").lower() == "true"

    ac = current_app.config.get("artist_commands")  # album commands
    try:
        return jsonify({"tracks": ac.top_tracks(artist_id, raw=raw_data)})

    except NotFoundError as e:
        raise e
    except Exception as e:
        raise SpotifyAPIError(f"Error retrieving album: {str(e)}")


@artist_bp.route("/top_albums/<artist_id>", methods=["GET"])
def get_artist_top_albums(artist_id):
    included_grps = ["album"]
    singles = request.args.get(
        "include_singles", "false").lower() == "true"
    appearsOn = request.args.get(
        "include_appears_on", "false").lower() == "true"
    compilation = request.args.get(
        "include_compilation", "false").lower() == "true"
    ac = current_app.config.get("artist_commands")  # album commands
    if singles:
        included_grps.append("single")
    if appearsOn:
        included_grps.append("appears_on")

    if compilation:
        included_grps.append("compilation")

    try:
        return jsonify({"albums": ac.top_albums(artist_id,  included_grps)})

    except NotFoundError as e:
        raise e
    except Exception as e:
        raise SpotifyAPIError(f"Error retrieving album: {str(e)}")


@artist_bp.route("/genres/<artist_id>", methods=["GET"])
def get_artist_genres(artist_id):

    ac = current_app.config.get("artist_commands")  # album commands
    try:
        return jsonify({"genres": ac.get_artist_genres(artist_id,)})

    except NotFoundError as e:
        raise e
    except Exception as e:
        raise SpotifyAPIError(f"Error retrieving album: {str(e)}")
