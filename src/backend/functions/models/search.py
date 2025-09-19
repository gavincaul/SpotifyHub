from pprint import pprint


class Search:
    def __init__(self, spotify_manager):
        self.sp = spotify_manager.get_spotify_client()
        self.spotify_manager = spotify_manager

    def search(self, query, types, market=None, limit=20, offset=0):
        """
        Perform a search against Spotify's catalog.

        :param query: str - search string (can include filters like 'artist:Drake track:One Dance')
        :param types: list[str] - allowed: "album", "artist", "playlist", "track", "show", "episode", "audiobook"
        :param market: str (ISO 3166-1 alpha-2), optional
        :param limit: int (default=20, max=50)
        :param offset: int (default=0, max=1000)
        :param include_external: str, optional ("audio")
        :return: dict of raw Spotify API results
        """
        return self.sp.search(
            q=query,
            type=",".join(types),
            market=market,
            limit=limit,
            offset=offset,
        )

    def search_tracks(self, query, market=None, limit=20, offset=0):
        results = self.search(
            query, ["track"], market, limit, offset)
        # return [[item["name"], item["id"]] for item in results["tracks"]["items"]]

    def search_artists(self, query, market=None, limit=20, offset=0):
        results = self.search(
            query, ["artist"], market, limit, offset)
        return [[item["name"], item["id"]] for item in results["artists"]["items"]]

    def search_albums(self, query, market=None, limit=20, offset=0):
        results = self.search(
            query, ["album"], market, limit, offset)

        # return [[item["name"], item["id"]] for item in results["albums"]["items"]]

    def search_playlists(self, query, market=None, limit=20, offset=0, include_external=None):
        results = self.search(
            query, ["playlist"], market, limit, offset, include_external)
        # return [[item["name"], item["id"]] for item in results["playlists"]["items"]]
