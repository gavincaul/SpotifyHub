

from ...utils.utils import missing_file_url


class Song:
    def __init__(self, spotify_manager, track_id, data=None):
        self.sp = spotify_manager.get_spotify_client()
        self.data = data
        self.track_id = track_id
        self.spotify_manager = spotify_manager

    def get_track(self):
        if self.data is None:
            self.data = self.sp.track(self.track_id)
        return self.data

    def get_track_name(self):
        self.get_track()
        return self.data["name"]

    def get_track_album(self):
        self.get_track()
        album = {"name": self.data["album"]["name"],
                 "id": self.data["album"]["id"]}
        return album

    def get_track_length(self):
        self.get_track()

        return self.data["duration_ms"]  # in milliseconds

    def get_track_popularity(self):
        self.get_track()

        return self.data["popularity"]

    def get_track_image(self):
        self.get_track()

        try:
            album_images = self.data.get("album", {}).get("images", [])
            if album_images and len(album_images) > 0:
                return {
                    "large": album_images[0].get("url", missing_file_url),
                    "medium": album_images[1].get("url", missing_file_url) if len(album_images) > 1 else missing_file_url,
                    "small": album_images[2].get("url", missing_file_url) if len(album_images) > 2 else missing_file_url,
                }
            return {
                "large": missing_file_url,
                "medium": missing_file_url,
                "small": missing_file_url,
            }
        except TypeError as e:
            print("ERROR: img is null {e}")
            return missing_file_url

    def get_track_artists(self):
        self.get_track()
        artists = [{"name": artist["name"], "id": artist["id"]}
                   for artist in self.data["artists"]]
        return artists

    def is_track_explicit(self):
        self.get_track()

        return self.data["explicit"]

    def get_track_url(self):
        self.get_track()

        return self.data["external_urls"]["spotify"]

    def get_track_id(self):
        return self.track_id

    def get_track_number(self):
        self.get_track()
        return self.data["track_number"]


'''
{
    "album": {
        "album_type": "album",
        "total_tracks": 9,
        "available_markets": ["AR", "BO", "BR", "CA", "CL", "CO", "CR", "DO", "EC", "SV", "GT", "HN", "HK", "MY", "MX", "NI", "PA", "PY", "PE", "PH", "SG", "TW", "UY", "US", "ID", "TH", "VN", "ZA", "SA", "AE", "BH", "QA", "OM", "KW", "EG", "MA", "DZ", "TN", "LB", "JO", "PS", "IN", "KR", "BD", "PK", "LK", "GH", "KE", "NG", "TZ", "UG", "AG", "BS", "BB", "BZ", "BT", "BW", "BF", "CV", "CW", "DM", "FJ", "GM", "GD", "GW", "GY", "HT", "JM", "KI", "LS", "LR", "MW", "MV", "ML", "MH", "FM", "NA", "NR", "NE", "PW", "PG", "PR", "WS", "ST", "SN", "SC", "SL", "SB", "KN", "LC", "VC", "SR", "TL", "TO", "TT", "TV", "VU", "AZ", "BN", "BI", "KH", "CM", "TD", "KM", "GQ", "SZ", "GA", "GN", "LA", "MO", "MR", "MN", "NP", "RW", "TG", "ZW", "BJ", "MG", "MU", "MZ", "AO", "CI", "DJ", "ZM", "CD", "CG", "IQ", "LY", "VE", "ET"],
        "external_urls": {
            "spotify": "https://open.spotify.com/album/3ShtO5VCYa3ctlR5uzLWBa"
        },
        "href": "https://api.spotify.com/v1/albums/3ShtO5VCYa3ctlR5uzLWBa",
        "id": "3ShtO5VCYa3ctlR5uzLWBa",
        "images": [
            {
                "url": "https://i.scdn.co/image/ab67616d0000b2738718f18aca81c2f4961946f4",
                "height": 640,
                "width": 640
            },
            {
                "url": "https://i.scdn.co/image/ab67616d00001e028718f18aca81c2f4961946f4",
                "height": 300,
                "width": 300
            },
            {
                "url": "https://i.scdn.co/image/ab67616d000048518718f18aca81c2f4961946f4",
                "height": 64,
                "width": 64
            }
        ],
        "name": "Promises",
        "release_date": "2021-03-26",
        "release_date_precision": "day",
        "type": "album",
        "uri": "spotify:album:3ShtO5VCYa3ctlR5uzLWBa",
        "artists": [
            {
                "external_urls": {
                    "spotify": "https://open.spotify.com/artist/2AR42Ur9PcchQDtEdwkv4L"
                },
                "href": "https://api.spotify.com/v1/artists/2AR42Ur9PcchQDtEdwkv4L",
                "id": "2AR42Ur9PcchQDtEdwkv4L",
                "name": "Floating Points",
                "type": "artist",
                "uri": "spotify:artist:2AR42Ur9PcchQDtEdwkv4L"
            },
            {
                "external_urls": {
                    "spotify": "https://open.spotify.com/artist/3JLUCojZaHrX2LaUkSj7Ud"
                },
                "href": "https://api.spotify.com/v1/artists/3JLUCojZaHrX2LaUkSj7Ud",
                "id": "3JLUCojZaHrX2LaUkSj7Ud",
                "name": "Pharoah Sanders",
                "type": "artist",
                "uri": "spotify:artist:3JLUCojZaHrX2LaUkSj7Ud"
            }
        ]
    },
    "artists": [
        {
            "external_urls": {
                "spotify": "https://open.spotify.com/artist/2AR42Ur9PcchQDtEdwkv4L"
            },
            "href": "https://api.spotify.com/v1/artists/2AR42Ur9PcchQDtEdwkv4L",
            "id": "2AR42Ur9PcchQDtEdwkv4L",
            "name": "Floating Points",
            "type": "artist",
            "uri": "spotify:artist:2AR42Ur9PcchQDtEdwkv4L"
        },
        {
            "external_urls": {
                "spotify": "https://open.spotify.com/artist/3JLUCojZaHrX2LaUkSj7Ud"
            },
            "href": "https://api.spotify.com/v1/artists/3JLUCojZaHrX2LaUkSj7Ud",
            "id": "3JLUCojZaHrX2LaUkSj7Ud",
            "name": "Pharoah Sanders",
            "type": "artist",
            "uri": "spotify:artist:3JLUCojZaHrX2LaUkSj7Ud"
        },
        {
            "external_urls": {
                "spotify": "https://open.spotify.com/artist/5yxyJsFanEAuwSM5kOuZKc"
            },
            "href": "https://api.spotify.com/v1/artists/5yxyJsFanEAuwSM5kOuZKc",
            "id": "5yxyJsFanEAuwSM5kOuZKc",
            "name": "London Symphony Orchestra",
            "type": "artist",
            "uri": "spotify:artist:5yxyJsFanEAuwSM5kOuZKc"
        }
    ],
    "available_markets": ["AR", "BO", "BR", "CA", "CL", "CO", "CR", "DO", "EC", "SV", "GT", "HN", "HK", "MY", "MX", "NI", "PA", "PY", "PE", "PH", "SG", "TW", "UY", "US", "ID", "TH", "VN", "ZA", "SA", "AE", "BH", "QA", "OM", "KW", "EG", "MA", "DZ", "TN", "LB", "JO", "PS", "IN", "KR", "BD", "PK", "LK", "GH", "KE", "NG", "TZ", "UG", "AG", "BS", "BB", "BZ", "BT", "BW", "BF", "CV", "CW", "DM", "FJ", "GM", "GD", "GW", "GY", "HT", "JM", "KI", "LS", "LR", "MW", "MV", "ML", "MH", "FM", "NA", "NR", "NE", "PW", "PG", "PR", "WS", "ST", "SN", "SC", "SL", "SB", "KN", "LC", "VC", "SR", "TL", "TO", "TT", "TV", "VU", "AZ", "BN", "BI", "KH", "CM", "TD", "KM", "GQ", "SZ", "GA", "GN", "LA", "MO", "MR", "MN", "NP", "RW", "TG", "ZW", "BJ", "MG", "MU", "MZ", "AO", "CI", "DJ", "ZM", "CD", "CG", "IQ", "LY", "VE", "ET"],
    "disc_number": 1,
    "duration_ms": 384151,
    "explicit": false,
    "external_ids": {
        "isrc": "USLB12010001"
    },
    "external_urls": {
        "spotify": "https://open.spotify.com/track/0QkT7SfXL9eR6tuQ7xb9ya"
    },
    "href": "https://api.spotify.com/v1/tracks/0QkT7SfXL9eR6tuQ7xb9ya",
    "id": "0QkT7SfXL9eR6tuQ7xb9ya",
    "name": "Movement 1",
    "popularity": 38,
    "preview_url": null,
    "track_number": 1,
    "type": "track",
    "uri": "spotify:track:0QkT7SfXL9eR6tuQ7xb9ya",
    "is_local": false
}
'''
