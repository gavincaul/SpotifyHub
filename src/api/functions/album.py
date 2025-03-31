
class Album:
    def __init__(self, spotify_manager):
        self.sp = spotify_manager.get_spotify_client()
        self.data = None

    def get_album(self, album_id):
        return self.sp.album(album_id)