from flask import Blueprint, jsonify, current_app

currentuser_bp = Blueprint("currentuser", __name__)


@currentuser_bp.route("/", methods=["GET"])
def get_current_user():
    try:
        currentuser_commands = current_app.config["currentuser_commands"]
        return jsonify(currentuser_commands.serialize_current_user())
    except Exception as e:
        return jsonify({"error": str(e)}), 500
