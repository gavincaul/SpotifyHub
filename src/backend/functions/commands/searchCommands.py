from ...utils.errors import *
from ...utils.utils import missing_file_url


class SearchCommands:
    def __init__(self, spotify_manager):
        self.spotify_manager = spotify_manager
        self.sp = spotify_manager.get_spotify_client()

    def search(self, query, search_type, limit=20, offset=0):
        """
        General search endpoint.
        Args:
            query (str): Search string
            search_type (str): Comma-separated types: track, album, artist, playlist
            limit (int): Max results per type
            offset (int): Pagination offset
        Returns:
            dict: Spotify search results
        """
        try:
            response = self.sp.search(
                q=query, type=search_type, limit=limit, offset=offset)
            data = {}
            match search_type:
                case "track":

                    data["tracks"] = [
                        {
                            "id": t["id"],
                            "name": t.get("name", "Unknown Name"),
                            "artists": [{a.get("name", "Unknown Artist"): a.get("id", "Unknown Artist ID")} for a in t.get("artists", [])],
                            "album": t.get("album", {}).get("name", "Unknown Album"),
                            "images": {"large": t["album"]["images"][0]["url"] if len(t["album"]["images"]) > 0 else missing_file_url, "medium": t["album"]["images"][1]["url"] if len(t["album"]["images"]) > 1 else missing_file_url, "small": t["album"]["images"][2]["url"] if len(t["album"]["images"]) > 2 else missing_file_url},
                            "duration_ms": t.get("duration_ms"),
                            "href": t.get("external_urls", {}).get("spotify"),
                        }
                        for t in response["tracks"]["items"] if t is not None
                    ]

                case "album":
    
                    data["albums"] = [
                        {
                            "id": a["id"],
                            "name": a.get("name", "Unknown Name"),
                            "artists": [{t.get("name", "Unknown Artist"): t.get("id", "Unknown Artist ID")} for t in a.get("artists", [])],
                            "album_type": a.get("album_type", "Unknown Album Type"),
                            "release_date": a.get("release_date"),
                            "images": {"large": a["images"][0]["url"] if len(a["images"]) > 0 else missing_file_url, "medium": a["images"][1]["url"] if len(a["images"]) > 1 else missing_file_url, "small": a["images"][2]["url"] if len(a["images"]) > 2 else missing_file_url},
                            "total_tracks": a.get("total_tracks"),
                            "href": a.get("external_urls", {}).get("spotify"),
                        }
                        for a in response["albums"]["items"] if a is not None
                    ]

                case "artist":

                    data["artists"] = [
                        {
                            "id": ar["id"],
                            "name": ar.get("name", "Unknown Name"),
                            "popularity": ar.get("popularity", "Unknown Popularity"),
                            "genres": ar.get("genres", []),
                            "followers": ar.get("followers", {}).get("total"),
                            "genres": ar.get("genres", []),
                            "images": {"large": ar["images"][0]["url"] if len(ar["images"]) > 0 else missing_file_url, "medium": ar["images"][1]["url"] if len(ar["images"]) > 1 else missing_file_url, "small": ar["images"][2]["url"] if len(ar["images"]) > 2 else missing_file_url},
                            "href": ar.get("external_urls", {}).get("spotify"),
                        }
                        for ar in response["artists"]["items"] if ar is not None
                    ]

                case "playlist":
                    
                    data["playlists"] = [
                        {
                           "collaborative": p.get("collaborative", False),
                           "public": p.get("public", True),
                           "description": p.get("description", "Unknown Description"),
                           "id": p["id"],
                           "name": p.get("name", "Unknown Name"),
                           "owner": {p.get("owner", {}).get("display_name", "Unknown Name"): p.get("owner",{}).get("id", "Unknown ID")},
                           "followers": p.get("followers", {}).get("total"),
                           "image_url": p.get("images", [])[0].get("url", missing_file_url),
                           "href": p.get("external_urls", {}).get("spotify"),
                           "total_tracks": p.get("tracks", {}).get("total", 0)
                        }
                        for p in response["playlists"]["items"] if p is not None
                    ]

            return data
        except Exception as e:
            print(e)
            raise Exception(f"Spotify search failed: {str(e)}")
