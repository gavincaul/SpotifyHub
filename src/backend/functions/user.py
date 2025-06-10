from functions.playlist import Playlist 

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
    
    def get_user_playlists(self, total=None):
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
    
    def get_user_following(self, total=None):
        if self.data is None:
            self.data = self.sp.user(self.user_id)

        following = []
        limit = 50 
        after = None
        fetched = 0

        while True:
            remaining = total - fetched if total else limit
            fetch_limit = min(limit, remaining)

            result = self.sp.current_user_followed_artists(limit=fetch_limit, after=after)
            artists = result["artists"]["items"]
            following.extend(artists)

            fetched += len(artists)

            if len(artists) < fetch_limit:
                break  

            after = artists[-1]["id"]

            if total and fetched >= total:
                break 

        return following
    