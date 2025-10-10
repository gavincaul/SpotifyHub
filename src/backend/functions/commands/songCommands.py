from ..models.song import Song
from ...utils.errors import *

class SongCommands:
    def __init__(self, spotify_manager):
        self.spotify_manager = spotify_manager
        self.song_cache = {}

    # ---------- Validation ----------
    def _validate_song_id(self, song_id):
        if not song_id or not isinstance(song_id, str) or song_id.strip() == "":
            raise BadRequestError("Song ID is required")
        return song_id.strip()

    # ---------- Centralized Error Handling ----------
    def _handle_song_operation(self, song_id, operation):
        song_id = self._validate_song_id(song_id)
        try:
            return operation(song_id)
        except SpotifyException as e:
            raise map_spotify_error(e, "song", song_id)
        except Exception as e:
            raise TrackOperationError(f"Unexpected error in song operation: {str(e)}")

    # ---------- Song Management ----------
    def check_song(self, song_id):
        def operation(song_id):
            if song_id in self.song_cache:
                return self.song_cache[song_id]
            song_obj = Song(self.spotify_manager, track_id=song_id)
            self.song_cache[song_id] = song_obj
            return song_obj
        return self._handle_song_operation(song_id, operation)

    def check_exists(self, song_id):
        def operation(song_id):
            if song_id in self.song_cache:
                return True
            try:
                data = self.spotify_manager.sp.track(song_id)
                song_obj = Song(self.spotify_manager, song_id, data=data)
                self.song_cache[song_id] = song_obj
                return True
            except SpotifyException as e:
                if e.http_status in (400, 404):
                    return False
                raise
        return self._handle_song_operation(song_id, operation)

    def get_song(self, song_id):
        def operation(song_id):
            return self.check_song(song_id)
        return self._handle_song_operation(song_id, operation)

    # ---------- User Actions ----------

    def get_song_info(self, song_id, raw=False):
        def operation(song_id):
            songObj = self.check_song(song_id)
            if raw: return songObj.get_track()
            data = {
                "name": songObj.get_track_name(),
                "id": songObj.get_track_id(),
                "artists": songObj.get_track_artists(),
                "album": songObj.get_track_album(),
                "imgs": songObj.get_track_image(),
                "length": songObj.get_track_length(),
                "explicit": songObj.is_track_explicit(),
                "href": songObj.get_track_url(),
                "track_number": songObj.get_track_number(),
                "popularity": songObj.get_track_popularity()

            }
            return data
        return self._handle_song_operation(song_id, operation)

    def save_song(self, song_id, current_user):
        def operation(song_id):
            if not current_user:
                raise UnauthorizedError("You must login first")
            current_user.saved_tracks_add([song_id])
            return {"message": f"Song {song_id} saved to your library"}
        return self._handle_song_operation(song_id, operation)

    def unsave_song(self, song_id, current_user):
        def operation(song_id):
            if not current_user:
                raise UnauthorizedError("You must login first")
            current_user.saved_tracks_delete([song_id])
            return {"message": f"Song {song_id} removed from your library"}
        return self._handle_song_operation(song_id, operation)

    def add_song_to_playlist(self, song_id, playlist_id, current_user):
        def operation(song_id):
            if not current_user:
                raise UnauthorizedError("You must login first")
            current_user.playlist_add_items(song_id, playlist_id)
            return {"message": f"Song {song_id} added to playlist {playlist_id}"}
        return self._handle_song_operation(song_id, operation)

    def remove_song_from_playlist(self, song_id, playlist_id, current_user):
        def operation(song_id):
            if not current_user:
                raise UnauthorizedError("You must login first")
            current_user.playlist_remove_items(song_id, playlist_id)
            return {"message": f"Song {song_id} removed from playlist {playlist_id}"}
        return self._handle_song_operation(song_id, operation)

    def check_song_on_playlist(self, song_id, playlist_tracks):
        def operation(song_id):
            return playlist_tracks.get(song_id, "")
        return self._handle_song_operation(song_id, operation)
