from .currentUserRoutes import check_logged_in
from flask import Blueprint, jsonify, current_app, request
from ...utils.errors import *
import base64

playlist_bp = Blueprint("playlist", __name__)


@playlist_bp.route("/check_exists/<playlist_id>", methods=["GET"])
def check_playlist_exists(playlist_id):
    try:
        playlist_commands = current_app.config["playlist_commands"]
        exists = playlist_commands.check_exists(playlist_id)
        return jsonify({"exists": exists})
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    except SpotifyException as e:
        raise map_spotify_error(e, "playist", playlist_id)
    except Exception as e:
        raise PlaylistOperationError(
            f"Unexpected error retrieving playlist: {str(e)}")


@playlist_bp.route("/get/<playlist_id>", methods=["GET"])
def get_playlist(playlist_id):
    try:
        playlist_commands = current_app.config["playlist_commands"]
        raw_data = request.args.get("raw", "false").lower() == "true"
        data = playlist_commands.get_playlist_info(playlist_id, raw=raw_data)
        return jsonify(data)
    except SpotifyException as e:
        raise map_spotify_error(e, "playlist", playlist_id)
    except Exception as e:
        raise PlaylistOperationError(
            f"Unexpected error retrieving playlist: {str(e)}")


@playlist_bp.route("/tracks/<playlist_id>", methods=["GET"])
def get_playlist_tracks(playlist_id):
    check_logged_in(PlaylistOperationError)
    try:
        playlist_commands = current_app.config["playlist_commands"]
        raw_data = request.args.get("raw", "false").lower() == "true"
        total = request.args.get("total", None)
        if total:
            if total.isnumeric():
                total = int(total)
        else:
            total = None
        tracks = playlist_commands.get_playlist_tracks(
            playlist_id, total, raw_data)
        return jsonify({"tracks": tracks})
    except SpotifyException as e:
        raise map_spotify_error(e, "playlist", playlist_id)
    except Exception as e:
        raise PlaylistOperationError(
            f"Unexpected error retrieving playlist tracks: {str(e)}")


@playlist_bp.route("/image/<playlist_id>", methods=["GET"])
def get_playlist_image(playlist_id):
    try:
        playlist_commands = current_app.config["playlist_commands"]
        playlist = playlist_commands.get_playlist(playlist_id)
        image_url = playlist.get_playlist_image()
        return jsonify({"image_url": image_url})
    except SpotifyException as e:
        raise map_spotify_error(e, "playlist", playlist_id)
    except Exception as e:
        raise PlaylistOperationError(
            f"Unexpected error retrieving playlist image: {str(e)}")


@playlist_bp.route("/upload/cover/<playlist_id>", methods=["PUT"])
def upload_playlist_cover(playlist_id):
    try:
        check_logged_in(PlaylistOperationError)
        playlist_commands = current_app.config["playlist_commands"]

        image_file = request.files.get("image")
        if request.is_json:
            data = request.get_json()
            image_url = data.get("url")

        # Support FormData with URL field too (optional)
        if not image_url:
            image_url = request.form.get("url")
        print(f"Received image_file: {image_file}, image_url: {image_url}")
        if image_file and image_file.filename != "":
            image_data = image_file.read()
            if len(image_data) > 256 * 1024:
                return jsonify({"error": "Image file size exceeds 256KB"}), 400
            # Convert to base64
            image_b64 = base64.b64encode(image_data).decode("utf-8")
            playlist_commands.upload_playlist_cover(playlist_id, image_b64)

        elif image_url and image_url.strip() != "":
            # Fetch image from URL
            resp = requests.get(image_url.strip())
            if resp.status_code != 200:
                return jsonify({"error": "Failed to fetch image from URL"}), 400
            image_data = resp.content
            if len(image_data) > 256 * 1024:
                return jsonify({"error": "Image from URL exceeds 256KB"}), 400
            image_b64 = base64.b64encode(image_data).decode("utf-8")
            playlist_commands.upload_playlist_cover(playlist_id, image_b64)

        else:
            return jsonify({"error": "No image file or URL provided"}), 400

        return jsonify({"message": "Playlist cover image updated successfully"})

    except SpotifyException as e:
        raise map_spotify_error(e, "playlist", playlist_id)
    except Exception as e:
        raise PlaylistOperationError(
            f"Unexpected error uploading playlist cover image: {str(e)}"
        )


@playlist_bp.route("/intersect", methods=["POST"])
def intersect_playlists():
    try:
        check_logged_in(PlaylistOperationError)
        playlist_commands = current_app.config["playlist_commands"]

        data = request.get_json()  # Expect JSON body
        p1 = data.get("p1")
        p2 = data.get("p2")
        p3 = data.get("p3")
        if not all([p1, p2, p3]):
            return jsonify({"error": "All three playlist IDs are required"}), 400
        p1_tracks = playlist_commands.get_playlist_track_ids(p1)
        p2_tracks = playlist_commands.get_playlist_track_ids(p2)
        shared_ids = playlist_commands.intersect_playlists(
            p1_tracks, p2_tracks, p3)
        return jsonify({
            "playlist_id": p3,
            "shared_track_count": len(shared_ids),
            "shared_tracks": shared_ids
        }), 200

    except SpotifyException as e:
        raise map_spotify_error(e, "playlist", p1)
    except Exception as e:
        raise PlaylistOperationError(
            f"Unexpected error intersecting playlists: {str(e)}"
        )


@playlist_bp.route("/union", methods=["POST"])
def union_playlists():
    try:
        check_logged_in(PlaylistOperationError)
        playlist_commands = current_app.config["playlist_commands"]

        data = request.get_json()  # Expect JSON body
        p1 = data.get("p1")
        p2 = data.get("p2")
        p3 = data.get("p3")
        if not all([p1, p2, p3]):
            return jsonify({"error": "All three playlist IDs are required"}), 400
        p1_tracks = playlist_commands.get_playlist_track_ids(p1)
        p2_tracks = playlist_commands.get_playlist_track_ids(p2)
        shared_ids = playlist_commands.union_playlists(
            p1_tracks, p2_tracks, p3)
        return jsonify({
            "playlist_id": p3,
            "total_unique_track_count": len(shared_ids),
            "total_unique_tracks": shared_ids
        }), 200

    except SpotifyException as e:
        raise map_spotify_error(e, "playlist", p1)
    except Exception as e:
        raise PlaylistOperationError(
            f"Unexpected error unioning playlists: {str(e)}"
        )


@playlist_bp.route("/differentiate", methods=["POST"])
def differentiate_playlists():
    try:
        check_logged_in(PlaylistOperationError)
        playlist_commands = current_app.config["playlist_commands"]

        data = request.get_json()  # Expect JSON body
        p1 = data.get("p1")
        p2 = data.get("p2")
        p3 = data.get("p3")
        if not all([p1, p2, p3]):
            return jsonify({"error": "All three playlist IDs are required"}), 400
        p1_tracks = playlist_commands.get_playlist_track_ids(p1)
        p2_tracks = playlist_commands.get_playlist_track_ids(p2)
        diff_ids = playlist_commands.differentiate_playlists(
            p1_tracks, p2_tracks, p3)
        return jsonify({
            "playlist_id": p3,
            "differentiated_track_count": len(diff_ids),
            "differentiated_tracks": diff_ids
        }), 200

    except SpotifyException as e:
        raise map_spotify_error(e, "playlist", p1)
    except Exception as e:
        raise PlaylistOperationError(
            f"Unexpected error differentiating playlists: {str(e)}"
        )


@playlist_bp.route("/move_tracks/<playlist_id>", methods=["PUT"])
def move_tracks(playlist_id):
    check_logged_in(PlaylistOperationError)
    try:

        playlist_commands = current_app.config["playlist_commands"]
        data = request.get_json()
        from_positions = data.get("fromPositions")
        to_position = data.get("toPosition")
        if playlist_id is None or not from_positions or to_position is None:
            return jsonify({"error": "playlist_id, from_positions, and to_position are required"}), 400
        if not isinstance(from_positions, list) or not all(isinstance(pos, int) for pos in from_positions):
            return jsonify({"error": "from_positions must be a list of integers"}), 400
        if not isinstance(to_position, int) or to_position < 0:
            return jsonify({"error": "to_position must be a non-negative integer"}), 400
        playlist = playlist_commands.get_playlist(playlist_id)
        pl = playlist.get_playlist_length()
        clean_positions = []
        for pos in from_positions:
            try:
                pos = int(pos)
            except (ValueError, TypeError):
                return jsonify({"error": "All from_positions must be non-negative integers"}), 400
            if 0 <= pos <= pl:
                clean_positions.append(pos - 1)

        placement = to_position + \
            len(clean_positions)-1 if to_position + \
            len(clean_positions) < pl else pl

        playlist.move_tracks(clean_positions, placement)
        return jsonify({
            "message": f"Moved {len(clean_positions)} tracks to start at position {placement} in playlist {playlist_id}"
        }), 200

    except SpotifyException as e:
        raise map_spotify_error(e, "playlist", playlist_id)
    except Exception as e:
        raise PlaylistOperationError(
            f"Unexpected error moving tracks in playlist: {str(e)}"
        )


@playlist_bp.route("/add/<playlist_id>", methods=["PUT"])
def add_to_playlist(playlist_id):
    check_logged_in(PlaylistOperationError)

    try:
        playlist_commands = current_app.config["playlist_commands"]

        track_id = request.args.get("track_id")
        position = request.args.get("position")
        if not track_id:
            return jsonify({"error": "track_id is required"}), 400
        if position is not None:
            try:
                position = int(position)
                if position < 0:
                    raise ValueError()
            except ValueError:
                return jsonify({"error": "position must be a non-negative integer"}), 400

        playlist_commands.add_tracks(
            playlist_id,
            track_id=[track_id],
            position=position
        )

        return jsonify({"message": f"Added track {track_id} to playlist {playlist_id}{f' at position {position}' if position else ''}"}), 200

    except SpotifyException as e:
        raise map_spotify_error(e, "playlist", playlist_id)
    except Exception as e:
        raise PlaylistOperationError(
            f"Unexpected error adding tracks in playlist: {str(e)}"
        )

@playlist_bp.route("/get/artists_tracks/<playlist_id>", methods=["GET"])
def get_artists_on_playlist(playlist_id):
    try:
        playlist_commands = current_app.config["playlist_commands"]
        artists = request.args.getlist("artists")
        print(artists)
        data = playlist_commands.get_artist_tracks_on_playlists(playlist_id, artists)   
        return jsonify(data)
    except SpotifyException as e:
        raise map_spotify_error(e, "playlist", playlist_id)
    except Exception as e:
        raise PlaylistOperationError(
            f"Unexpected error adding tracks in playlist: {str(e)}"
        )
