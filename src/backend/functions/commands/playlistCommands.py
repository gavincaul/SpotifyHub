from functions.models.playlist import Playlist

class PlaylistCommands:
    def __init__(self, spotify_manager):
        self.spotify_manager = spotify_manager

    playlist_list = {}

    def check_playlist(self, playlist_id=None):
        if playlist_id in self.playlist_list:
            return self.playlist_id[playlist_id]
    
        self.self.playlist_list[playlist_id] = Playlist(self.spotify_manager, playlist_id=playlist_id)
        return self.playlist_list[playlist_id]