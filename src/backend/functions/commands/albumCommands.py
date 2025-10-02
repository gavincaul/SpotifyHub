from functions.models.album import Album

class AlbumCommands:
    def __init__(self, spotify_manager):
        self.spotify_manager = spotify_manager
        self.album_cache = {}

    def check_album(self, album_id=None):
        if album_id in self.album_cache:
            return self.album_cache[album_id]
    
        self.album_cache[album_id] = Album(self.spotify_manager, album_id)
        return self.album_cache[album_id]

    def check_exists(self, album_id):
        if album_id in self.album_cache:
            return True
        try:
            data = self.spotify_manager.sp.album(album_id)
            album_obj = Album(self.spotify_manager, album_id, data=data)
            self.album_cache[album_id] = album_obj
            return True
        except self.spotify_manager.sp.exceptions.SpotifyException as e:
            return e.http_status not in [400, 404]
        

    def get_album_info(self, album_id=None):

        album_obj = self.check_album(album_id)
        print(f"Name: {album_obj.get_album_name()}")
        print(f"Type: {album_obj.get_album_type()}")
        print(f"Total Tracks: {album_obj.get_album_total_tracks()}")
        print(f"Artists: {[ar.get_artist_name() for ar in album_obj.get_album_artists()]}")
        print(f"Cover URL: {album_obj.get_album_cover()}")

    def track_list(self, album_id=None):
        album_obj = self.check_album(album_id)
        tracks = album_obj.get_album_tracks()
        return tracks

    def save(self, album_id=None, current_user=None):
        if not current_user:
            print("You must login first")
            return
        try:
            current_user.saved_albums_add([album_id])
            print("Album saved to your library")
        except Exception as e:
            print(f"Unable to save album: {e}")

    def unsave(self, album_id=None, current_user=None):
        if not current_user:
            print("You must login first")
            return
        try:
            current_user.saved_albums_remove([album_id])
            print("Album removed from your library")
        except Exception as e:
            print(f"Unable to remove album: {e}")

    def get_album_artists(self, album_id=None):
        album_obj = self.check_album(album_id)
        artists = album_obj.get_album_artists()
        return artists
    
    
