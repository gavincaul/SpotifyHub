from ..models.playlist import Playlist
from ...utils.errors import *


class PlaylistCommands:
    def __init__(self, spotify_manager):
        self.spotify_manager = spotify_manager
        self.playlist_cache = {}

    # ---------- Validation ----------
    def _validate_playlist_id(self, playlist_id):
        if not playlist_id or not isinstance(playlist_id, str) or playlist_id.strip() == "":
            raise BadRequestError("Playlist ID is required")
        return playlist_id.strip()

    # ---------- Centralized Error Handling ----------
    def _handle_playlist_operation(self, playlist_id, operation):
        playlist_id = self._validate_playlist_id(playlist_id)
        try:
            return operation(playlist_id)
        except SpotifyException as e:
            raise map_spotify_error(e, "playlist", playlist_id)
        except Exception as e:
            raise PlaylistOperationError(
                f"Unexpected error in playlist operation: {str(e)}"
            )

    # ---------- Playlist Management ----------
    def check_playlist(self, playlist_id):
        def operation(playlist_id):
            if playlist_id in self.playlist_cache:
                return self.playlist_cache[playlist_id]
            playlist_obj = Playlist(
                self.spotify_manager, playlist_id=playlist_id)
            self.playlist_cache[playlist_id] = playlist_obj
            return playlist_obj
        return self._handle_playlist_operation(playlist_id, operation)

    def check_exists(self, playlist_id):
        def operation(playlist_id):
            if playlist_id in self.playlist_cache:
                return True
            try:
                data = self.spotify_manager.sp.playlist(playlist_id)
                playlist_obj = Playlist(
                    self.spotify_manager, playlist_id, data=data)
                self.playlist_cache[playlist_id] = playlist_obj
                return True
            except SpotifyException as e:
                if e.http_status in (400, 404):
                    return False
                raise
        return self._handle_playlist_operation(playlist_id, operation)

    def get_playlist(self, playlist_id):
        def operation(playlist_id):
            return self.check_playlist(playlist_id)
        return self._handle_playlist_operation(playlist_id, operation)

    # ---------- Track Operations ----------
    def get_playlist_info(self, playlist_id, raw):
        def operation(playlist_id):
            playlist = self.get_playlist(playlist_id)

            if raw:
                return playlist.get_playlist()
            data = {
                "name": playlist.get_playlist_name(),
                "description": playlist.get_playlist_description(),
                "image": playlist.get_playlist_image(),
                "owner": playlist.get_playlist_owner(),
                "follower_count": playlist.get_playlist_follower_count(),
                "visibility": playlist.get_playlist_visibility(),
                "length": playlist.get_playlist_length(),
                "collaborative": playlist.get_playlist_collaborative(),
                "id": playlist.playlist_id,
                "url": playlist.get_playlist_url()
            }
            return data
        return self._handle_playlist_operation(playlist_id, operation)

    def get_playlist_track_ids(self, playlist_id):
        def operation(playlist_id):
            playlist = self.check_playlist(playlist_id)
            return playlist.get_playlist_track_ids(playlist.get_playlist_length())
        return self._handle_playlist_operation(playlist_id, operation)

    def get_playlist_tracks(self, playlist_id, limit=None, raw=False):
        def operation(playlist_id):
            playlist = self.check_playlist(playlist_id)
            if not limit:
                total = playlist.get_playlist_length()
            elif limit > playlist.get_playlist_length():
                total = playlist.get_playlist_length()
            else:
                total = limit
            if raw:
                return playlist.get_playlist_tracks(total)
            else:
                data = playlist.get_playlist_tracks_info(total)
            return data
        return self._handle_playlist_operation(playlist_id, operation)

    def move_tracks(self, playlist_id, from_positions, to_position):
        def operation(playlist_id):
            playlist = self.check_playlist(playlist_id)
            return playlist.move_tracks(from_positions, to_position)

        return self._handle_playlist_operation(playlist_id, operation)

    def replace_track_exchange(self, playlist_id, track_R_id, track_A_id, position):
        def operation(playlist_id):
            playlist = self.check_playlist(playlist_id)
            if playlist.remove_specific_track(track_R_id, position):
                return playlist.add_specific_track(track_A_id, position)
            return False
        return self._handle_playlist_operation(playlist_id, operation)

    def upload_playlist_cover(self, playlist_id, image_b64):
        """Upload playlist cover image (Base64)"""
        def operation(playlist_id):
            playlist = self.check_playlist(playlist_id)
            return playlist.upload_cover_image_raw(image_b64)
        return self._handle_playlist_operation(playlist_id, operation)

    # ---------- Playlist Set Operations ----------
    def intersect_playlists(self, p1_tracks, p2_tracks, p3_id):
        ids1 = set(p1_tracks)
        ids2 = set(p2_tracks)
        shared_ids = ids1 & ids2

        def operation(p3_id):
            playlist = self.check_playlist(p3_id)
            playlist.add_tracks(list(shared_ids))
            return list(shared_ids)
        result = self._handle_playlist_operation(p3_id, operation)
        return result

    def union_playlists(self, p1_tracks, p2_tracks, p3_id):
        ids1 = set(p1_tracks)
        ids2 = set(p2_tracks)
        shared_ids = ids1 | ids2

        def operation(p3_id):
            playlist = self.check_playlist(p3_id)
            playlist.add_tracks(list(shared_ids))
            return list(shared_ids)
        result = self._handle_playlist_operation(p3_id, operation)
        return result

    def differentiate_playlists(self, p1_tracks, p2_tracks, p3_id):
        """Add to p3 the tracks in p1 but not in p2"""
        ids1 = set(p1_tracks)
        ids2 = set(p2_tracks)
        shared_ids = ids1 - ids2

        def operation(p3_id):
            playlist = self.check_playlist(p3_id)
            playlist.add_tracks(list(shared_ids))
            return list(shared_ids)
        result = self._handle_playlist_operation(p3_id, operation)
        return result

    def add_tracks(self, playlist_id, track_id, position=None):
        def operation(playlist_id):
            playlist = self.check_playlist(playlist_id)
            if position is not None:
                print(position)
                return playlist.add_specific_tracks(track_id=track_id, position=position-1)
            else:
                return playlist.add_tracks(track_ids=track_id)
        return self._handle_playlist_operation(playlist_id, operation)

    def get_artist_tracks_on_playlists(self, playlist_id, artists):
        def operation(playlist_id):
            playlist = self.check_playlist(playlist_id)
            total = playlist.get_playlist_length()
            # Map artist_id -> {artist_name: [(track_name, track_id), ...]}
            artist_set = {artist_id: {} for artist_id in artists}

            track_data = playlist.get_playlist_tracks_info(total)
            for track in track_data:

                track_name = track.get("name")
                track_id = track.get("id")

                for artist in track.get("artist_data", []):
                    artist_id = artist.get("id")
                    artist_name = artist.get("name")
                    if artist_id in artist_set:
                        if artist_name not in artist_set[artist_id]:
                            artist_set[artist_id][artist_name] = []
                        artist_set[artist_id][artist_name].append(
                            (track_name, track_id))

            return artist_set
        return self._handle_playlist_operation(playlist_id, operation)

    # ---------- Cache Management ----------

    def clear_cache(self, playlist_id=None):
        if playlist_id:
            playlist_id = self._validate_playlist_id(playlist_id)
            self.playlist_cache.pop(playlist_id, None)
            return f"Cache cleared for playlist {playlist_id}"
        else:
            self.playlist_cache.clear()
            return "All playlist cache cleared"

    def get_cached_playlists_count(self):
        return len(self.playlist_cache)
