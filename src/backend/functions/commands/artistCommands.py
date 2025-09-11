from functions.models.artist import Artist

class ArtistCommands:
    def __init__(self, spotify_manager):
        self.spotify_manager = spotify_manager

    artist_list = {}

    def check_artist(self, artist_id=None):
        if artist_id in self.artist_list:
            return self.artist_list[artist_id]
    
        self.artist_list[artist_id] = Artist(self.spotify_manager, artist_id=artist_id)
        return self.artist_list[artist_id]

    def get_artist_info(self, artist_id=None):
        
        artist_obj = self.check_artist(artist_id)
        print(f"Name: {artist_obj.get_artist_name()}")
        print(f"Genres: {', '.join(artist_obj.get_artist_genres())}")
        print(f"Followers: {artist_obj.get_artist_followers()}")
        print(f"Popularity: {artist_obj.get_artist_popularity()}")
        print(f"Image URL: {artist_obj.get_artist_image_url()}")    


    def top_tracks(self, artist_id=None, country="US"):
        artist_obj = self.check_artist(artist_id)
        tracks = artist_obj.get_artist_top_tracks(country=country)
        return tracks
    
    def top_albums(self, artist_id=None):
        artist_obj = self.check_artist(artist_id)
        poll = input("Include compliations and features? (y/n): ").strip().lower()
        if poll == 'y':
            include_groups = "album,single,appears_on,compilation"
        else:
            include_groups = "album,single"
        albums = artist_obj.get_artist_albums(include_groups=include_groups, limit=50)
        return albums
   