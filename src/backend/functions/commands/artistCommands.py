from functions.models.artist import Artist
from functions.models.search import Search


class ArtistCommands:
    def __init__(self, spotify_manager):
        self.spotify_manager = spotify_manager

    artist_list = {}

    def check_artist(self, artist_id=None):
        if artist_id in self.artist_list:
            return self.artist_list[artist_id]

        self.artist_list[artist_id] = Artist(
            self.spotify_manager, artist_id=artist_id)
        return self.artist_list[artist_id]

    def get_artist_info(self, artist_id=None):

        artist_obj = self.check_artist(artist_id)
        return artist_obj

    def top_tracks(self, artist_id=None, country="US"):
        artist_obj = self.check_artist(artist_id)
        tracks = artist_obj.get_artist_top_tracks(country=country)
        return tracks

    def top_albums(self, artist_id=None):
        artist_obj = self.check_artist(artist_id)
        poll = input(
            "Include compliations and features? (y/n): ").strip().lower()
        if poll == 'y':
            include_groups = "album,single,appears_on,compilation"
        else:
            include_groups = "album,single"
        albums = artist_obj.get_artist_albums(
            include_groups=include_groups, limit=50)
        return albums

    def get_artist_genres(self, artist_id=None):
        artist_obj = self.check_artist(artist_id)
        genres = artist_obj.get_artist_genres()
        return genres

    def search_artist(self, search_value, offset=0, limit=20):
        if not search_value:
            return []

        if not hasattr(self, "search_obj"):
            from functions.models.search import Search
            self.search_obj = Search(self.spotify_manager)

        results = self.search_obj.search_artists(
            query=search_value,
            market='US',
            limit=limit,
            offset=offset,
        )

        return results
