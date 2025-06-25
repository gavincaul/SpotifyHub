


class Album:
    def __init__(self, spotify_manager, album_id):
        self.sp = spotify_manager.get_spotify_client()
        self.data = None
        self.album_id = album_id
        self.spotify_manager = spotify_manager

    def get_album(self):
        if self.data == None:
            self.data = self.sp.album(self.album_id)
        return self.data

    def get_album_name(self):
        if self.data == None:
            self.data = self.get_album()
        return self.data["name"]

    def get_album_type(self):
        if self.data == None:
            self.data = self.get_album()
        return self.data["type"]

    def get_album_total_tracks(self):
        if self.data == None:
            self.data = self.get_album()
        return self.data["total_tracks"]

    def get_album_artists(self):
        from .artist import Artist
        if self.data == None:
            self.data = self.get_album()
        artist_array = []
        
        for artist in self.data["artists"]:
            artist_array.append(
                Artist(spotify_manager=self.spotify_manager, artist_id=artist["id"]))
        return artist_array

    def get_album_tracks(self):
        from .song import Song
        if self.data == None:
            self.data = self.get_album()
        track_array = []
        for track in self.data["tracks"]["items"]:
            track_array.append(
                Song(spotify_manager=self.spotify_manager, track_id=track["id"]))
        return track_array

    def get_album_cover(self):
        if self.data == None:
            self.data = self.get_album()
        try:
            return self.data["images"][0]["url"]
        except TypeError as e:
            print("ERROR: img is null {e}")
            return "https://static.thenounproject.com/png/3647578-200.png"


