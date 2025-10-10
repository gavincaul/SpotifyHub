from ..models.currentuser import CurrentUser
from ...utils.errors import *
from ...utils.utils import missing_file_url
import spotipy
import logging


class CurrentUserCommands:
    def __init__(self, spotify_manager):
        self.spotify_manager = spotify_manager
        self.current_user = None

    def _get_or_restore_current_user(self):
        """Return current_user; attempt to restore from Redis if None"""
        if self.current_user:
            return self.current_user

        # Scan Redis for spotify_token:* keys
        try:
            token_keys = self.spotify_manager.redis_client.keys(
                "spotify_token:*")
            if token_keys:
                key = token_keys[0]
                token_info = self.spotify_manager.redis_client.get(key)
                if token_info:
                    import json
                    token_info = json.loads(token_info)
                    self.spotify_manager.current_user_id = key.split(":")[1]

                    # Rehydrate Spotify client
                    self.spotify_manager.sp = spotipy.Spotify(
                        auth=token_info["access_token"]
                    )

                    # Validate token by fetching current user
                    self.spotify_manager.sp.me()  # <-- this may raise SpotifyException

                    from ..models.currentuser import CurrentUser
                    self.current_user = CurrentUser(self.spotify_manager)
                    print(
                        f"✅ Restored current_user from Redis: {self.spotify_manager.current_user_id}")
                    return self.current_user
        except SpotifyException as e:
            print(f"⚠️ Spotify error restoring token from Redis: {e}")
            raise map_spotify_error(e, "current_user", "self")
        except Exception as e:
            print(f"⚠️ Failed to restore token from Redis: {e}")
            raise

        return None

    # ---------- Validation + Error Handling ----------
    def _handle_currentuser_operation(self, operation):
        """Centralized error handling for current user operations"""
        try:
            return operation()
        except SpotifyException as e:
            raise map_spotify_error(e, "current_user", "self")
        except Exception as e:
            raise CurrentUserOperationError(
                f"Unexpected error in current user operation: {str(e)}"
            )

    # ---------- Core User Management ----------
    def login(self):
        """Login user and set current_user"""
        def operation():
            if self.current_user is not None:
                return {"message": f"Already logged in as {self.current_user.user_id}"}

            # Attempt to restore user from cached Redis token
            cached_user_id = self.spotify_manager.current_user_id
            if cached_user_id and self.spotify_manager.user_cache_handler:
                cached_token = self.spotify_manager.user_cache_handler.get_cached_token()
                if cached_token:
                    # Rehydrate Spotify client with cached token
                    self.spotify_manager.sp = spotipy.Spotify(
                        auth=cached_token["access_token"])
                    self.current_user = CurrentUser(self.spotify_manager)
                    return {"message": f"Restored session for {cached_user_id}"}

            # No cached token, proceed with OAuth login
            if not self.spotify_manager._create_oauth():
                raise UnauthorizedError("Login failed or cancelled")

            user_id = self.spotify_manager.get_current_user_id()
            if not user_id:
                raise SpotifyAPIError(
                    "Failed to retrieve user info after login")

            self.current_user = CurrentUser(self.spotify_manager)
            return {"message": f"Logged in as {user_id}"}

        return self._handle_currentuser_operation(operation)

    def logout(self):
        """Log out current user and clear user session"""
        def operation():
            if not self.current_user:
                raise UnauthorizedError("No user currently logged in")

            # Call SpotifyManager to clear session and delete cached token
            self.spotify_manager.logout()

            # Clear CurrentUser object
            self.current_user = None

            return {"message": "User logged out successfully"}

        return self._handle_currentuser_operation(operation)

    def get_profile(self, raw=False):
        """Return current user profile data"""
        def operation():
            if not self.current_user:
                raise UnauthorizedError("No user logged in")
            user_data = self.current_user.get_user_profile()

            if raw:
                return user_data
            data = {
                "user_id": self.current_user.user_id,
                "display_name": user_data.get("display_name", "Unknown Name"),
                "email": user_data.get("email"),
                "followers": user_data["followers"].get("total"),
                "product": user_data.get("product"),
                "country": user_data.get("country"),
                "images": {"small": user_data["images"][1].get("url", "") if user_data["images"] else missing_file_url, "large": self.current_user.data["images"][0].get("url", "") if self.current_user.data["images"] else missing_file_url}
            }
            return data

        return self._handle_currentuser_operation(operation)

    # ---------- User Library ----------
    def save_album(self, album_id=None):
        """Save album to user's library"""
        def operation():
            if not self.current_user:
                raise UnauthorizedError("You must login first")
            self.current_user.saved_albums_add([album_id])
            return {"message": f"Album {album_id} saved to your library"}

        return self._handle_currentuser_operation(operation)

    def remove_album(self, album_id=None):
        """Remove album from user's library"""
        def operation():
            if not self.current_user:
                raise UnauthorizedError("You must login first")
            self.current_user.saved_albums_remove([album_id])
            return {"message": f"Album {album_id} removed from your library"}

        return self._handle_currentuser_operation(operation)

    # ---------- Playlists ----------
    def create_playlist(self, playlist_name, description="", public=True, collaborative=False):
        """Create a new user playlist"""
        def operation():
            if not self.current_user:
                raise UnauthorizedError("You must login first")
            return self.current_user.create_playlist(
                playlist_name, description, public, collaborative
            )

        return self._handle_currentuser_operation(operation)

    def delete_playlist(self, playlist_id):
        """Delete a playlist"""
        def operation():
            if not self.current_user:
                raise UnauthorizedError("You must login first")
            return self.current_user.delete_playlist(playlist_id)

        return self._handle_currentuser_operation(operation)

    # ---------- Settings ----------
    def get_settings(self):
        """Retrieve user app settings from database"""
        def operation():
            if not self.current_user:
                raise UnauthorizedError("You must login first")
            return self.settings_manager.get_user_settings(self.current_user.user_id)

        return self._handle_currentuser_operation(operation)

    def update_settings(self, settings_dict):
        """Update user app settings"""
        def operation():
            if not self.current_user:
                raise UnauthorizedError("You must login first")
            return self.settings_manager.update_user_settings(
                self.current_user.user_id, settings_dict
            )

        return self._handle_currentuser_operation(operation)

    def get_top_tracks(self, time_range="medium_term", limit=10):
        """Get user's top tracks"""
        def operation():
            if not self.current_user:
                raise UnauthorizedError("You must login first")
            track_data = self.current_user.get_user_top_tracks(
                limit, time_range)
            data = [
                {"name": i.get("name", "Unknown Name"),
                 "id": i.get("id", "Unknown TrackID"),
                 "href": i["external_urls"].get("spotify", "Unknown URL"),
                 "duration_ms": i.get("duration_ms", 0),
                 "popularity": i.get("popularity", 0),

                 "album_data": {"name": i["album"].get("name", "Unknown Album Name"),
                                "type": i["album"].get("type", "Unknown Album Type"),
                                "id": i["album"].get("id", "Unknown Album ID"),
                                "cover": i["album"]["images"][0].get("url", missing_file_url) if i["album"]["images"] else missing_file_url,
                                },

                 "artist_data": [
                     {"name": p.get("name", "Unknown Artist Name"),
                      "id": p.get("id", "Unknown Artist ID")} for p in i["artists"]]}
                for i in track_data]
            return data

        return self._handle_currentuser_operation(operation)

    def get_top_artists(self, time_range="medium_term", limit=10):
        """Get user's top tracks"""
        def operation():
            if not self.current_user:
                raise UnauthorizedError("You must login first")
            artist_data = self.current_user.get_user_top_artists(
                limit, time_range)

            data = [{"name": i.get("name", "Unknown Name"),
                     "id": i.get("id", "Unknown ArtistID"),
                     "href": i["external_urls"].get("spotify", "Unknown URL"),
                     "popularity": i.get("popularity", 0),
                     "followers": i["followers"].get("total", 0),
                     "images": {"large": i["images"][0].get("url", missing_file_url) if i["images"] else missing_file_url,
                                "medium": i["images"][1].get("url", missing_file_url) if len(i["images"]) > 1 else missing_file_url,
                                "small": i["images"][2].get("url", missing_file_url) if len(i["images"]) > 2 else missing_file_url}
                     } for i in artist_data]
            return data

        return self._handle_currentuser_operation(operation)

    def unfollow_user(self, user_id):
        """Unfollow another user"""
        def operation():
            if not self.current_user:
                raise UnauthorizedError("You must login first")
            self.current_user.unfollow_user([user_id])  # list format
            return

        return self._handle_currentuser_operation(operation)

    def follow_user(self, user_id):
        """Follow another user"""
        def operation():
            if not self.current_user:
                raise UnauthorizedError("You must login first")
            self.current_user.follow_user([user_id])  # list format
            return

        return self._handle_currentuser_operation(operation)

    def unfollow_artist(self, artist_id):
        """Unfollow an artist"""
        def operation():
            if not self.current_user:
                raise UnauthorizedError("You must login first")
            self.current_user.unfollow_artist([artist_id])  # list format
            return

        return self._handle_currentuser_operation(operation)

    def follow_artist(self, artist_id):
        """Follow an artist"""
        def operation():
            if not self.current_user:
                raise UnauthorizedError("You must login first")
            self.current_user.follow_artist([artist_id])  # list format
            return

        return self._handle_currentuser_operation(operation)

    def follow_playlist(self, playlist_id):
        """Follow a playlist"""
        def operation():
            if not self.current_user:
                raise UnauthorizedError("You must login first")
            self.current_user.follow_playlist(playlist_id)
            return

        return self._handle_currentuser_operation(operation)

    def unfollow_playlist(self, playlist_id):
        """Unfollow a playlist"""
        def operation():
            if not self.current_user:
                raise UnauthorizedError("You must login first")
            self.current_user.unfollow_playlist(playlist_id)
            return

        return self._handle_currentuser_operation(operation)

    def delete_saved_tracks(self, track_id):
        """Delete a saved track"""
        def operation():
            if not self.current_user:
                raise UnauthorizedError("You must login first")
            self.current_user.saved_tracks_delete([track_id])
            return

        return self._handle_currentuser_operation(operation)

    def save_tracks(self, track_id):
        """Save a track"""
        def operation():
            if not self.current_user:
                raise UnauthorizedError("You must login first")
            self.current_user.saved_tracks_add([track_id])
            return

        return self._handle_currentuser_operation(operation)

    def delete_saved_albums(self, album_id):
        """Delete a saved album"""
        def operation():
            if not self.current_user:
                raise UnauthorizedError("You must login first")
            self.current_user.saved_albums_delete([album_id])
            return

        return self._handle_currentuser_operation(operation)

    def save_albums(self, album_id):
        """Save an album"""
        def operation():
            if not self.current_user:
                raise UnauthorizedError("You must login first")
            self.current_user.saved_albums_add([album_id])
            return

        return self._handle_currentuser_operation(operation)

    def get_devices(self):
        """Get user devices"""
        def operation():
            if not self.current_user:
                raise UnauthorizedError("You must login first")
            devices = self.current_user.get_user_devices()
            return devices

        return self._handle_currentuser_operation(operation)

    def get_playlists(self):
        """Get user playlists"""
        def operation():
            if not self.current_user:
                raise UnauthorizedError("You must login first")

            playlists = self.current_user.get_user_playlists()
            return playlists
        return self._handle_currentuser_operation(operation)

    def get_albums(self):
        """Get user albums"""
        def operation():
            if not self.current_user:
                raise UnauthorizedError("You must login first")

            albums = self.current_user.get_user_albums()
            return albums
        return self._handle_currentuser_operation(operation)

    def get_tracks(self):
        """Get user tracks"""
        def operation():
            if not self.current_user:
                raise UnauthorizedError("You must login first")

            tracks = self.current_user.get_user_tracks()
            return tracks
        return self._handle_currentuser_operation(operation)

    def get_artists(self):
        """Get user artists"""
        def operation():
            if not self.current_user:
                raise UnauthorizedError("You must login first")

            artists = self.current_user.get_user_artists()
            return artists
        return self._handle_currentuser_operation(operation)

    def get_library(self):
        """Get user Library"""
        def operation():
            if not self.current_user:
                raise UnauthorizedError("You must login first")
            playlists = self.current_user.get_user_playlists()
            albums = self.current_user.get_user_albums()
            tracks = self.current_user.get_user_tracks()
            artists = self.current_user.get_user_artists()
            data = {"playlists": playlists,
                    "albums": albums,
                    "tracks": tracks,
                    "artists": artists}
            return data
        return self._handle_currentuser_operation(operation)
