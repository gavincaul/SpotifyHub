class Artist:
    def __init__(self, spotify_manager, artist_id):
        self.sp = spotify_manager.get_spotify_client()
        self.data = None
        self.artist_id = artist_id
        self.spotify_manager = spotify_manager

    def get_artist(self):
        if self.data == None:
            self.data = self.sp.artist(self.artist_id)
        return self.data

    def get_artist_name(self):
        if self.data == None:
            self.data = self.get_artist()
        return self.data["name"]
    
    def get_artists(self, artist_ids):
        if artist_ids == None or len(artist_ids) == 0:
            return []
        if len(artist_ids) > 50:
            raise ValueError("Maximum of 50 artist IDs allowed")
        if len(artist_ids) == 1:
            return [self.sp.artist(artist_ids[0])]
        return self.sp.artists(artist_ids)["artists"]
    
    def get_artist_genres(self):
        if self.data == None:
            self.data = self.get_artist()
        return self.data["genres"]
    
    def get_artist_image_url(self):
        if self.data == None:
            self.data = self.get_artist()
        if len(self.data["images"]) > 0:
            return self.data["images"][0]["url"]
        return ""
    
    
    def get_artist_popularity(self):
        if self.data == None:
            self.data = self.get_artist()
        return self.data["popularity"]
    
    def get_artist_followers(self):
        if self.data == None:
            self.data = self.get_artist()
        return self.data["followers"]["total"]
    

    def get_artist_id(self):
        return self.artist_id
    
    def get_artist_top_tracks(self, country="US"):
        if self.data == None:
            self.data = self.get_artist()
        tracks = self.sp.artist_top_tracks(self.artist_id, country=country)["tracks"]
        from .song import Song
        track_list = []
        for t in tracks:
            t = Song(spotify_manager=self.spotify_manager, track_id=t["id"])
            track_list.append(t)
        return track_list

    
    def get_artist_albums(self, include_groups=None, limit=20, offset=0):
        if include_groups is None:
            include_groups = ["album", "single", "appears_on", "compilation"]
        albums = self.sp.artist_albums(self.artist_id, include_groups=include_groups, limit=limit, offset=offset)["items"]
        from .album import Album
        album_list = []
        for a in albums:
            a = Album(spotify_manager=self.spotify_manager, album_id=a["id"])
            album_list.append(a)
        return album_list