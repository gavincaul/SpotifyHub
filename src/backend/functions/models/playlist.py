

class Playlist:
    def __init__(self, spotify_manager, playlist_id):
        self.sp = spotify_manager.get_spotify_client()
        self.data = None
        self.playlist_id = playlist_id
        self.spotify_manager = spotify_manager

    def get_playlist(self):
        if self.data is None:
            self.data = self.sp.playlist(self.playlist_id)
        return self.data

    def get_playlist_length(self):
        if self.data is None:
            self.data = self.get_playlist()
        return self.data["tracks"]["total"]

    def get_playlist_name(self):
        if self.data is None:
            self.data = self.get_playlist()
        return self.data["name"]

    def get_playlist_image(self):
        if self.data is None:
            self.data = self.get_playlist()
        try:
            return self.data["images"][0]["url"]
        except TypeError as e:
            print("ERROR: img is null {e}")
            return "https://static.thenounproject.com/png/3647578-200.png"
    
    def get_playlist_tracks(self, total):
        if self.data is None:
            self.data = self.get_playlist()
        
        songs = []
        limit = 50
        offset = 0


        if total is None:
            result = self.sp.playlist_tracks(self.playlist_id, limit=limit, offset=offset)
            total = result["total"]
            songs.extend(result["items"])
            offset += len(result["items"])
        else:
            while len(songs) < total:
                result = self.sp.current_user_top_artists(limit=min(limit, total - offset), offset=offset)
                items = result["items"]
                if not items:
                    break
                songs.extend(items)
                offset += len(items)

        return songs
