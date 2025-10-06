from flask import Blueprint, jsonify, current_app

song_bp = Blueprint("song", __name__)


@song_bp.route("/<song_id>", methods=["GET"])
def get_song(song_id):
    try:
        song_commands = current_app.config["song_commands"]
        return jsonify(song_commands.serialize_song(song_id))
    except Exception as e:
        return jsonify({"error": str(e)}), 500
