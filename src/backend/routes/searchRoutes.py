from flask import Blueprint, jsonify, current_app, request

search_bp = Blueprint("search", __name__)


@search_bp.route("/", methods=["GET"])
def search():
    try:
        query = request.args.get("q")
        search_commands = current_app.config["search_commands"]
        return jsonify(search_commands.search(query))
    except Exception as e:
        return jsonify({"error": str(e)}), 500
