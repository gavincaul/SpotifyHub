from ..models.artist import Artist
from ..models.search import Search
from ...errors import *


class ArtistCommands:
    def __init__(self, spotify_manager):
        self.spotify_manager = spotify_manager
        self.artist_cache = {}
        self.search_obj = None

    def _validate_artist_id(self, artist_id):
        """Centralized input validation"""
        if not artist_id or not isinstance(artist_id, str) or artist_id.strip() == "":
            raise BadRequestError("Artist ID is required")
        return artist_id.strip()

    def _handle_artist_operation(self, artist_id, operation):
        """Centralized error handling for artist operations"""
        artist_id = self._validate_artist_id(artist_id)

        try:
            return operation(artist_id)
        except SpotifyException as e:
            raise map_spotify_error(e, "artist", artist_id)
        except Exception as e:
            raise ArtistOperationError(
                f"Unexpected error in artist operation: {str(e)}"
            )

    def check_artist(self, artist_id=None):
        """Check if artist exists and return artist object"""
        def operation(artist_id):
            if artist_id in self.artist_cache:
                return self.artist_cache[artist_id]

            artist_obj = Artist(self.spotify_manager, artist_id=artist_id)
            self.artist_cache[artist_id] = artist_obj
            return artist_obj

        return self._handle_artist_operation(artist_id, operation)

    def check_exists(self, artist_id=None):
        """Check if artist exists without full initialization"""
        def operation(artist_id):
            if artist_id in self.artist_cache:
                return True
            try:
                data = self.spotify_manager.sp.artist(artist_id)
                artist_obj = Artist(self.spotify_manager, artist_id, data=data)
                self.artist_cache[artist_id] = artist_obj
                return True
            except SpotifyException as e:
                if e.http_status in (400, 404):
                    return False
                raise

        return self._handle_artist_operation(artist_id, operation)

    def get_artist(self, artist_id=None):
        """Get full artist object"""
        def operation(artist_id):
            return self.check_artist(artist_id)

        return self._handle_artist_operation(artist_id, operation)

    def top_tracks(self, artist_id=None, country="US", raw=False):
        """Get artist's top tracks"""
        def operation(artist_id):
            artist_obj = self.check_artist(artist_id)
            return artist_obj.get_artist_top_tracks(country=country, raw=raw)

        return self._handle_artist_operation(artist_id, operation)

    def top_albums(self, artist_id=None, include_groups="album,single"):
        """Get artist's albums (configurable groups)"""
        def operation(artist_id):
            artist_obj = self.check_artist(artist_id)
            albums = artist_obj.get_artist_albums(
                include_groups=include_groups, limit=50
            )
            return albums

        return self._handle_artist_operation(artist_id, operation)

    def get_artist_genres(self, artist_id=None):
        """Get artist genres"""
        def operation(artist_id):
            artist_obj = self.check_artist(artist_id)
            return artist_obj.get_artist_genres()

        return self._handle_artist_operation(artist_id, operation)

    def search_artist(self, search_value, offset=0, limit=20):
        """Search for artists"""
        if not search_value:
            return []

        if not self.search_obj:
            self.search_obj = Search(self.spotify_manager)

        try:
            results = self.search_obj.search_artists(
                query=search_value,
                market='US',
                limit=limit,
                offset=offset,
            )
            return results
        except SpotifyException as e:
            raise map_spotify_error(e, "artist_search", search_value)
        except Exception as e:
            raise ArtistOperationError(
                f"Unexpected error in artist search: {str(e)}"
            )

    # Cache management
    def clear_cache(self, artist_id=None):
        """Clear cache for specific artist or entire cache"""
        if artist_id:
            artist_id = self._validate_artist_id(artist_id)
            self.artist_cache.pop(artist_id, None)
            return f"Cache cleared for artist {artist_id}"
        else:
            self.artist_cache.clear()
            return "All artist cache cleared"

    def get_cached_artists_count(self):
        """Get number of artists in cache"""
        return len(self.artist_cache)
