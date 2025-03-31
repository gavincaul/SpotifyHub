from src.api.functions.playlist import Playlist 

class User:
    def __init__(self, spotify_manager, user_id):
        self.sp = spotify_manager.get_spotify_client()
        self.spotify_manager = spotify_manager
        self.data = None
        self.playlists = []
        self.user_id = user_id

    def get_user_profile(self):
        if self.data == None:
            self.data = self.sp.user(self.user_id)
        return self.data
    
    def get_user_playlists(self):
        if self.playlists == []:
            offset=0
            user_playlists = self.sp.user_playlists(self.user_id, limit=50)
            total = user_playlists["total"]
            while(offset<total):
                for playlist in user_playlists["items"]:
                    self.playlists.append(Playlist(spotify_manager=self.spotify_manager, playlist_id=playlist["id"]))
                offset += 50
                user_playlists = self.sp.user_playlists(self.user_id, limit=50, offset=offset)
        return self.playlists