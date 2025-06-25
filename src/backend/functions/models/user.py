

class User:
    def __init__(self, spotify_manager, user_id):
        self.sp = spotify_manager.get_spotify_client()
        self.spotify_manager = spotify_manager
        self.data = None
        self.playlists = []
        self.user_id = user_id

    def get_user_profile(self):
        if self.data is None:
            self.data = self.sp.user(self.user_id)
        return self.data
    
    def get_user_playlists(self, total=None):
        from .playlist import Playlist
        if not self.playlists:
            offset = 0
            fetched = 0

        
            if not total:
                first_batch = self.sp.user_playlists(self.user_id, limit=50)
                total = first_batch["total"]

            while fetched < total:
                limit = min(50, total - fetched)
                user_playlists = self.sp.user_playlists(self.user_id, limit=limit, offset=offset)

                for playlist in user_playlists["items"]:
                    self.playlists.append(
                        Playlist(spotify_manager=self.spotify_manager, playlist_id=playlist["id"])
                    )

                fetched += len(user_playlists["items"])
                offset += limit

                if len(user_playlists["items"]) < limit:
                    break  

        return self.playlists
    
    

    
    