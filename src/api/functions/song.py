class Song:
    def __init__(self, spotify_manager):
        self.sp = spotify_manager.get_spotify_client()
        self.data = None

    def get_track(self, track_id):
        return self.sp.track(track_id)