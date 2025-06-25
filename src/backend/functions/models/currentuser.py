from .user import User

class CurrentUser(User):
    def __init__(self, spotify_manager):
        user_id = spotify_manager.get_current_user_id()
        if not user_id:
            raise ValueError("Unable to fetch current user ID.")
        super().__init__(spotify_manager, user_id)

    def get_user_top_tracks(self, total=None, time_range="medium_term"):
        if self.data is None:
            self.data = self.sp.user(self.user_id)

        top_tracks = []
        limit = 50
        offset = 0


        if total is None:
            result = self.sp.current_user_top_tracks(limit=limit, offset=offset, time_range=time_range)
            total = result["total"]
            top_tracks.extend(result["items"])
            offset += len(result["items"])
        else:
            while len(top_tracks) < total:
                result = self.sp.current_user_top_tracks(limit=min(limit, total - offset), offset=offset, time_range=time_range)
                items = result["items"]
                if not items:
                    break
                top_tracks.extend(items)
                offset += len(items)

        return top_tracks

    def get_user_top_artists(self, total=None, time_range="medium_term"):
        if self.data is None:
            self.data = self.sp.user(self.user_id)

        top_artists = []
        limit = 50
        offset = 0


        if total is None:
            result = self.sp.current_user_top_artists(limit=limit, offset=offset, time_range=time_range)
            total = result["total"]
            top_artists.extend(result["items"])
            offset += len(result["items"])
        else:
            while len(top_artists) < total:
                result = self.sp.current_user_top_artists(limit=min(limit, total - offset), offset=offset, time_range=time_range)
                items = result["items"]
                if not items:
                    break
                top_artists.extend(items)
                offset += len(items)

        return top_artists
    
    def follow_playlist(self, playlist_id):
        if self.data is None:
            self.data = self.sp.user(self.user_id)
        try:
            self.sp.current_user_follow_playlist(playlist_id)
            print(f"Successfully followed playlist")
        except Exception as e:
            print(f"Failed to follow playlist: {e}")

    def unfollow_playlist(self, playlist_id):
        if self.data is None:
            self.data = self.sp.user(self.user_id)
        try:
            self.sp.current_user_unfollow_playlist(playlist_id)
            print(f"Successfully unfollowed playlist")
        except Exception as e:
            print(f"Failed to follow playlist: {e}")
    
            

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