class Artist:
    def __init__(self, spotify_manager, artist_id):
        self.sp = spotify_manager.get_spotify_client()
        self.data = None
        self.artist_id = artist_id

    def get_artist(self):
        if self.data == None:
            self.data = self.sp.artist(self.artist_id)
        return self.data
