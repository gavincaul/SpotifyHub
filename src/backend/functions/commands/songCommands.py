from functions.models.song import Song

class SongCommands:
    def __init__(self, spotify_manager):
        self.spotify_manager = spotify_manager

    song_list = {}

    def check_song(self, song_id=None):
        if song_id in self.song_list:
            return self.song_list[song_id]
    
        self.song_list[song_id] = Song(self.spotify_manager, track_id=song_id)
        return self.song_list[song_id]
    
    def get_song_info(self, song_id=None):
        song_obj = self.check_song(song_id)
        print(f"Song Name: {song_obj.get_track_name()}")
        print(f"Artists: {', '.join([artist.get_artist_name() for artist in song_obj.get_track_artists()])}")
        print(f"Album: {song_obj.get_track_album().get_album_name()}")
        print(f"Duration (ms): {song_obj.get_track_length_ms()}")
        print(f"Popularity: {song_obj.get_track_popularity()}")
        print(f"Explicit: {song_obj.is_track_explicit()}")
        print(f"External URL: {song_obj.get_track_url()}")