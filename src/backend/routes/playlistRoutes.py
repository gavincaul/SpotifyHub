from flask import Blueprint, jsonify, current_app

playlist_bp = Blueprint("playlist", __name__)


@playlist_bp.route("/<playlist_id>", methods=["GET"])
def get_playlist(playlist_id):
    try:
        playlist_commands = current_app.config["playlist_commands"]
        return jsonify(playlist_commands.serialize_playlist(playlist_id))
    except Exception as e:
        return jsonify({"error": str(e)}), 500
