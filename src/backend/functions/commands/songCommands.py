from functions.models.song import Song


class SongCommands:
    def __init__(self, spotify_manager):
        self.spotify_manager = spotify_manager
        self.song_cache = {}

    def check_song(self, song_id=None):
        if song_id in self.song_cache:
            return self.song_cache[song_id]

        self.song_cache[song_id] = Song(self.spotify_manager, track_id=song_id)
        return self.song_cache[song_id]

    def check_exists(self, song_id):
        if song_id in self.song_cache:
            return True
        try:
            data = self.spotify_manager.sp.track(song_id)
            song_obj = Song(self.spotify_manager, song_id, data=data)
            self.song_cache[song_id] = song_obj
            return True
        except self.spotify_manager.sp.exceptions.SpotifyException as e:
            return e.http_status not in [400, 404]

    def get_song_info(self, song_id=None):
        song_obj = self.check_song(song_id)
        return song_obj

    def save_song(self, song_id=None, current_user=None):
        if not current_user:
            print("You must login first")
            return
        try:
            current_user.saved_tracks_add([song_id])
            print("Song saved to your library")
        except Exception as e:
            print(f"Unable to save Song: {e}")

    def unsave_song(self, song_id=None, current_user=None):
        if not current_user:
            print("You must login first")
            return
        try:
            current_user.saved_tracks_delete([song_id])
            print("Song unsaved from your library")
        except Exception as e:
            print(f"Unable to save Song: {e}")

    def add_song_to_playlist(self, song_id, playlist_id, current_user=None):
        if not current_user:
            print("You must login first")
            return
        try:
            current_user.playlist_add_items(song_id, playlist_id)
        except Exception as e:
            print(f"Unable to add song(s) to playlist: {e}")

    def remove_song_from_playlist(self, song_id, playlist_id, current_user=None):
        if not current_user:
            print("You must login first")
            return
        try:
            current_user.playlist_remove_items(
                song_id, playlist_id)
        except Exception as e:
            print(f"Unable to remove song(s) to playlist: {e}")

    def check_song_on_playlist(self, song_id, playlist_tracks):
        if playlist_tracks[song_id]:
            return playlist_tracks[song_id]
        return ""
