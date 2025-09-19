from functions.models.playlist import Playlist


class PlaylistCommands:
    def __init__(self, spotify_manager):
        self.spotify_manager = spotify_manager

    playlist_list = {}

    def check_playlist(self, playlist_id=None):
        if playlist_id in self.playlist_list:
            return self.playlist_id[playlist_id]

        self.playlist_list[playlist_id] = Playlist(
            self.spotify_manager, playlist_id=playlist_id)
        return self.playlist_list[playlist_id]

    def get_playlist_tracks(self, playlist_id=None):
        playlist = self.check_playlist(playlist_id)
        length = playlist.get_playlist_length()
        return playlist.get_playlist_tracks(length)

    def get_playlist_track_names(self, playlist_id=None):
        playlist = self.check_playlist(playlist_id)
        length = playlist.get_playlist_length()
        return playlist.get_playlist_track_names(length)
