from flask import Blueprint, jsonify, current_app, request
from ...utils.errors import *

search_bp = Blueprint("search", __name__)


@search_bp.route("/<query>", methods=["GET"])
def search(query):
    """Search Spotify for a query string."""
    try:
        if not query:
            return jsonify({"error": "Search input is required"}), 400
        type = request.args.get("search_type", None)
        if not type:
            return jsonify({"error": "Search type is required"}), 400
        limit = request.args.get("limit", 20)
        offset = request.args.get("offset", 0)
        if type not in ["album", "artist", "playlist", "track", "show", "episode", "audiobook"]:
            raise BadRequestError("Invalid type", type)
        search_commands = current_app.config["search_commands"]
        results = search_commands.search(
            query, search_type=type, limit=limit, offset=offset)
        return jsonify(results)
    except SpotifyException as e:
        raise map_spotify_error(e, "search", query)
    except Exception as e:
        raise ServerError(
            f"Unexpected error searching for {query}: {str(e)}"
        )