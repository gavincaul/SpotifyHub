from ..models.user import User
from ...utils.errors import *
from spotipy import SpotifyException
from ...utils.utils import missing_file_url


class UserCommands:
    def __init__(self, spotify_manager):
        self.spotify_manager = spotify_manager
        self.user_cache = {}

    # ---------- Validation ----------
    def _validate_user_id(self, user_id):
        if not user_id or not isinstance(user_id, str) or user_id.strip() == "":
            raise BadRequestError("User ID is required")
        return user_id.strip()

    # ---------- Centralized Error Handling ----------
    def _handle_user_operation(self, user_id, operation):
        user_id = self._validate_user_id(user_id)
        try:
            return operation(user_id)
        except SpotifyException as e:
            raise map_spotify_error(e, "user", user_id)
        except Exception as e:
            raise UserOperationError(
                f"Unexpected error in user operation: {str(e)}")

    # ---------- Core ----------
    def check_user(self, user_id=None):
        """
        Retrieve a User object, either from cache or by creating a new one.
        """
        user_id = self._validate_user_id(user_id)

        if user_id in self.user_cache:
            return self.user_cache[user_id]

        user_obj = User(self.spotify_manager, user_id=user_id)
        self.user_cache[user_id] = user_obj
        return user_obj

    def check_exists(self, user_id):
        """
        Verify whether a given user exists on Spotify.
        Caches the result if found.
        """
        user_id = self._validate_user_id(user_id)

        if user_id in self.user_cache:
            return True

        def _operation(uid):
            try:
                data = self.spotify_manager.sp.user(uid)
                user_obj = User(self.spotify_manager, uid, data=data)
                self.user_cache[uid] = user_obj
                return True
            except SpotifyException as e:
                return e.http_status not in [400, 404]
        return self._handle_user_operation(user_id, _operation)

    # ---------- Data Retrieval ----------
    def get_user_info(self, user_id, raw=False):
        """
        Return basic user info (delegated to the User model).
        """
        def _operation(uid):
            user_obj = self.check_user(uid)
            data = user_obj.get_user()
            if raw:
                return data
            images = data.get("images", [])
            return {
                "id": data.get("id"),
                "display_name": data.get("display_name"),
                "followers": data.get("followers", {}).get("total"),
                "images": {"large": images[0].get("url", missing_file_url) if len(images) > 0 else missing_file_url,
                           "small":  images[1].get("url", missing_file_url) if len(images) > 1 else missing_file_url},
                "href": data.get("external_urls", {}).get("spotify", ""),
            }

        return self._handle_user_operation(user_id, _operation)

    def get_user_playlists(self, user_id):
        """
        Retrieve playlists owned or followed by the user.
        """
        def _operation(uid):
            user_obj = self.check_user(uid)
            return user_obj.get_user_playlists()

        return self._handle_user_operation(user_id, _operation)

