from functions.models.playlist import Playlist


class PlaylistCommands:
    def __init__(self, spotify_manager):
        self.spotify_manager = spotify_manager
        self.playlist_cache = {}

    def check_playlist(self, playlist_id=None):
        if playlist_id in self.playlist_cache:
            return self.playlist_cache[playlist_id]

        self.playlist_cache[playlist_id] = Playlist(
            self.spotify_manager, playlist_id=playlist_id)
        return self.playlist_cache[playlist_id]

    def get_playlist_info(self, playlist_id=None):
        playlist_obj = self.check_playlist(playlist_id)
        return playlist_obj

    def check_exists(self, playlist_id):
        if playlist_id in self.playlist_cache:
            return True
        try:
            data = self.spotify_manager.sp.playlist(playlist_id)
            playlist_obj = Playlist(
                self.spotify_manager, playlist_id, data=data)
            self.playlist_cache[playlist_id] = playlist_obj
            return True
        except Exception as e:
            return e.http_status not in [400, 404]

    def get_playlist_tracks(self, playlist_id=None):
        playlist = self.check_playlist(playlist_id)
        length = playlist.get_playlist_length()
        return playlist.get_playlist_tracks(length)

    def get_playlist_track_names(self, playlist_id=None, length=20):
        playlist = self.check_playlist(playlist_id)
        length = playlist.get_playlist_length()
        return playlist.get_playlist_track_names(length)

    def get_playlist_track_names_and_positions(self, playlist_id=None, length=20):
        playlist = self.check_playlist(playlist_id)
        length = playlist.get_playlist_length()
        return playlist.get_playlist_track_names_and_positions(length)

    def upload_playlist_image(self, playlist_id=None, URL=None):
        playlist = self.check_playlist(playlist_id)
        return playlist.upload_cover_image(URL)

    def replace_track_exchange(self, playlist_id, track_R_id, track_A_id, position):
        playlist = self.check_playlist(playlist_id)
        if playlist.remove_specific_track(track_R_id, position):
            return playlist.add_specific_track(track_A_id, position)
        return False

    def intersect_playlists(self, p1_tracks, p2_tracks, p3):
        ids1 = {t[0] for t in p1_tracks}
        ids2 = {t[0] for t in p2_tracks}
        shared_ids = ids1 & ids2
        self.check_playlist(p3).add_tracks(list(shared_ids))

    def union_playlists(self, p1_tracks, p2_tracks, p3):
        ids1 = {t[0] for t in p1_tracks}
        ids2 = {t[0] for t in p2_tracks}
        shared_ids = ids1 | ids2
        self.check_playlist(p3).add_tracks(list(shared_ids))

    def differentiate_playlists(self, p1_tracks, p2_tracks, p3):
        """
        Finds the difference between playlists.
        differentiate  "p1-p2": Adds to p3 the tracks that are in p1 but not in p2.
        """
        ids1 = {t[0] for t in p1_tracks}
        ids2 = {t[0] for t in p2_tracks}
        diff_ids = ids1 - ids2
        self.check_playlist(p3).add_tracks(list(diff_ids))

    def move_track(self, playlist_id, from_position, to_position):
        playlist = self.check_playlist(playlist_id)
        if to_position>1: to_position+=1
        return playlist.move_track(from_position, to_position)
