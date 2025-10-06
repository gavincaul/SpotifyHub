from flask import Blueprint, jsonify, current_app

user_bp = Blueprint("user", __name__)


@user_bp.route("/<user_id>", methods=["GET"])
def get_user(user_id):
    try:
        user_commands = current_app.config["user_commands"]
        return jsonify(user_commands.serialize_user(user_id))
    except Exception as e:
        return jsonify({"error": str(e)}), 500
