from ..models.album import Album
from ...utils.errors import *


class AlbumCommands:
    def __init__(self, spotify_manager):
        self.spotify_manager = spotify_manager
        self.album_cache = {}

    def _validate_album_id(self, album_id):
        """Centralized input validation"""
        if not album_id or not isinstance(album_id, str) or album_id.strip() == "":
            raise BadRequestError("Album ID is required")
        return album_id.strip()

    def _handle_album_operation(self, album_id, operation):
        """Centralized error handling for album operations"""
        album_id = self._validate_album_id(album_id)

        try:
            return operation(album_id)
        except SpotifyException as e:
            raise map_spotify_error(e, "album", album_id)
        except Exception as e:
            raise AlbumOperationError(
                f"Unexpected error in album operation: {str(e)}")

    def check_album(self, album_id=None):
        """Check if album exists and return album object"""
        def operation(album_id):
            if album_id in self.album_cache:
                return self.album_cache[album_id]

            album_obj = Album(self.spotify_manager, album_id)
            self.album_cache[album_id] = album_obj
            return album_obj

        return self._handle_album_operation(album_id, operation)

    def check_exists(self, album_id=None):
        """Check if album exists without full initialization"""
        def operation(album_id):
            if album_id in self.album_cache:
                return True

            try:
                data = self.spotify_manager.sp.album(album_id)
                album_obj = Album(self.spotify_manager, album_id, data=data)
                self.album_cache[album_id] = album_obj
                return True
            except SpotifyException as e:

                if e.http_status in (400, 404):
                    return False
                raise

        return self._handle_album_operation(album_id, operation)

    def get_album_track_list(self, album_id=None, positions=False):
        """Get album tracks"""
        def operation(album_id):
            album_obj = self.check_album(album_id)
            return album_obj.get_album_tracks(positions)

        return self._handle_album_operation(album_id, operation)

    def get_album_artists(self, album_id=None):
        """Get Album Artist"""
        def operation(album_id):
            album_obj = self.check_album(album_id)
            artists = album_obj.get_album_artist_data()
            artists_data = []
            for a in artists:
                artists_data.append(
                    {"id": a["id"], "name": a["name"], "url": a["external_urls"].get("spotify", "No URL")})
            return artists_data
        return self._handle_album_operation(album_id, operation)

    def save(self, album_id=None, current_user=None):
        """Save album to user's library"""
        def operation(album_id):
            if not current_user:
                raise UnauthorizedError("You must login first")

            current_user.saved_albums_add([album_id])
            return "Album saved to your library"

        return self._handle_album_operation(album_id, operation)

    def unsave(self, album_id=None, current_user=None):
        """Remove album from user's library"""
        def operation(album_id):
            if not current_user:
                raise UnauthorizedError("You must login first")

            current_user.saved_albums_remove([album_id])
            return "Album removed from your library"

        return self._handle_album_operation(album_id, operation)

    # Additional utility methods with proper error handling

    def clear_cache(self, album_id=None):
        """Clear cache for specific album or entire cache"""
        if album_id:
            album_id = self._validate_album_id(album_id)
            self.album_cache.pop(album_id, None)
            return f"Cache cleared for album {album_id}"
        else:
            self.album_cache.clear()
            return "All album cache cleared"

    def get_cached_albums_count(self):
        """Get number of albums in cache"""
        return len(self.album_cache)
