from src.api.functions.song import Song
from src.api.functions.artist import Artist


class Album:
    def __init__(self, spotify_manager, album_id):
        self.sp = spotify_manager.get_spotify_client()
        self.data = None
        self.album_id = album_id
        self.spotify_manager = spotify_manager

    def get_album(self):
        if self.data == None:
            self.data = self.sp.album(self.album_id)
        return self.data

    def get_album_name(self):
        if self.data == None:
            self.data = self.get_album()
        return self.data["name"]

    def get_album_type(self):
        if self.data == None:
            self.data = self.get_album()
        return self.data["type"]

    def get_album_total_tracks(self):
        if self.data == None:
            self.data = self.get_album()
        return self.data["total_tracks"]

    def get_album_artists(self):
        if self.data == None:
            self.data = self.get_album()
        artist_array = []
        for artist in self.data["artists"]:
            artist_array.append(
                Artist(spotify_manager=self.spotify_manager, artist_id=artist["id"]))
        return artist_array

    def get_album_tracks(self):
        if self.data == None:
            self.data = self.get_album()
        track_array = []
        for track in self.data["tracks"]["items"]:
            track_array.append(
                Song(spotify_manager=self.spotify_manager, track_id=track["id"]))
        return track_array

    def get_album_cover(self):
        if self.data == None:
            self.data = self.get_album()
        try:
            return self.data["images"][0]["url"]
        except TypeError as e:
            print("ERROR: img is null {e}")
            return "https://static.thenounproject.com/png/3647578-200.png"


'''
Example JSON

{
  "album_type": "album",
  "total_tracks": 9,
  "available_markets": ["AR", "BO", "BR", "CA", "CL", "CO", "CR", "DO", "EC", "SV", "GT", "HN", "HK", "MY", "MX", "NI", "PA", "PY", "PE", "PH", "SG", "TW", "UY", "US", "ID", "TH", "VN", "ZA", "SA", "AE", "BH", "QA", "OM", "KW", "EG", "MA", "DZ", "TN", "LB", "JO", "PS", "IN", "KR", "BD", "PK", "LK", "GH", "KE", "NG", "TZ", "UG", "AG", "BS", "BB", "BZ", "BT", "BW", "BF", "CV", "CW", "DM", "FJ", "GM", "GD", "GW", "GY", "HT", "JM", "KI", "LS", "LR", "MW", "MV", "ML", "MH", "FM", "NA", "NR", "NE", "PW", "PG", "PR", "WS", "ST", "SN", "SC", "SL", "SB", "KN", "LC", "VC", "SR", "TL", "TO", "TT", "TV", "VU", "AZ", "BN", "BI", "KH", "CM", "TD", "KM", "GQ", "SZ", "GA", "GN", "LA", "MO", "MR", "MN", "NP", "RW", "TG", "ZW", "BJ", "MG", "MU", "MZ", "AO", "CI", "DJ", "ZM", "CD", "CG", "IQ", "LY", "VE", "ET"],
  "external_urls": {
    "spotify": "https://open.spotify.com/album/3ShtO5VCYa3ctlR5uzLWBa"
  },
  "href": "https://api.spotify.com/v1/albums/3ShtO5VCYa3ctlR5uzLWBa?locale=en-US%2Cen%3Bq%3D0.9%2Ces%3Bq%3D0.8",
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
  ],
  "tracks": {
    "href": "https://api.spotify.com/v1/albums/3ShtO5VCYa3ctlR5uzLWBa/tracks?offset=0&limit=50&locale=en-US,en;q%3D0.9,es;q%3D0.8",
    "limit": 50,
    "next": null,
    "offset": 0,
    "previous": null,
    "total": 9,
    "items": [
      {
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
        "external_urls": {
          "spotify": "https://open.spotify.com/track/0QkT7SfXL9eR6tuQ7xb9ya"
        },
        "href": "https://api.spotify.com/v1/tracks/0QkT7SfXL9eR6tuQ7xb9ya",
        "id": "0QkT7SfXL9eR6tuQ7xb9ya",
        "name": "Movement 1",
        "preview_url": null,
        "track_number": 1,
        "type": "track",
        "uri": "spotify:track:0QkT7SfXL9eR6tuQ7xb9ya",
        "is_local": false
      },
      {
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
        "duration_ms": 151327,
        "explicit": false,
        "external_urls": {
          "spotify": "https://open.spotify.com/track/5KqceyQkpADmpVrGW6armI"
        },
        "href": "https://api.spotify.com/v1/tracks/5KqceyQkpADmpVrGW6armI",
        "id": "5KqceyQkpADmpVrGW6armI",
        "name": "Movement 2",
        "preview_url": null,
        "track_number": 2,
        "type": "track",
        "uri": "spotify:track:5KqceyQkpADmpVrGW6armI",
        "is_local": false
      },
      {
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
        "duration_ms": 152088,
        "explicit": false,
        "external_urls": {
          "spotify": "https://open.spotify.com/track/2ZB1ms89d3xpy92gvTDQC5"
        },
        "href": "https://api.spotify.com/v1/tracks/2ZB1ms89d3xpy92gvTDQC5",
        "id": "2ZB1ms89d3xpy92gvTDQC5",
        "name": "Movement 3",
        "preview_url": null,
        "track_number": 3,
        "type": "track",
        "uri": "spotify:track:2ZB1ms89d3xpy92gvTDQC5",
        "is_local": false
      },
      {
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
        "duration_ms": 151770,
        "explicit": false,
        "external_urls": {
          "spotify": "https://open.spotify.com/track/4JNMmiYUmLQiv83k96qNdT"
        },
        "href": "https://api.spotify.com/v1/tracks/4JNMmiYUmLQiv83k96qNdT",
        "id": "4JNMmiYUmLQiv83k96qNdT",
        "name": "Movement 4",
        "preview_url": null,
        "track_number": 4,
        "type": "track",
        "uri": "spotify:track:4JNMmiYUmLQiv83k96qNdT",
        "is_local": false
      },
      {
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
        "duration_ms": 265224,
        "explicit": false,
        "external_urls": {
          "spotify": "https://open.spotify.com/track/6lAsz2ai52QsfWX4f4PlqH"
        },
        "href": "https://api.spotify.com/v1/tracks/6lAsz2ai52QsfWX4f4PlqH",
        "id": "6lAsz2ai52QsfWX4f4PlqH",
        "name": "Movement 5",
        "preview_url": null,
        "track_number": 5,
        "type": "track",
        "uri": "spotify:track:6lAsz2ai52QsfWX4f4PlqH",
        "is_local": false
      },
      {
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
        "duration_ms": 530894,
        "explicit": false,
        "external_urls": {
          "spotify": "https://open.spotify.com/track/5i0EqAX50KcKNgMDMHZndM"
        },
        "href": "https://api.spotify.com/v1/tracks/5i0EqAX50KcKNgMDMHZndM",
        "id": "5i0EqAX50KcKNgMDMHZndM",
        "name": "Movement 6",
        "preview_url": null,
        "track_number": 6,
        "type": "track",
        "uri": "spotify:track:5i0EqAX50KcKNgMDMHZndM",
        "is_local": false
      },
      {
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
        "duration_ms": 568933,
        "explicit": false,
        "external_urls": {
          "spotify": "https://open.spotify.com/track/5Zg3BH3Xipq3GQZCRyhAX8"
        },
        "href": "https://api.spotify.com/v1/tracks/5Zg3BH3Xipq3GQZCRyhAX8",
        "id": "5Zg3BH3Xipq3GQZCRyhAX8",
        "name": "Movement 7",
        "preview_url": null,
        "track_number": 7,
        "type": "track",
        "uri": "spotify:track:5Zg3BH3Xipq3GQZCRyhAX8",
        "is_local": false
      },
      {
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
        "duration_ms": 442961,
        "explicit": false,
        "external_urls": {
          "spotify": "https://open.spotify.com/track/0KRliRKOaqc3vT8t9noppI"
        },
        "href": "https://api.spotify.com/v1/tracks/0KRliRKOaqc3vT8t9noppI",
        "id": "0KRliRKOaqc3vT8t9noppI",
        "name": "Movement 8",
        "preview_url": null,
        "track_number": 8,
        "type": "track",
        "uri": "spotify:track:0KRliRKOaqc3vT8t9noppI",
        "is_local": false
      },
      {
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
        "duration_ms": 150092,
        "explicit": false,
        "external_urls": {
          "spotify": "https://open.spotify.com/track/1Q3TP11UOqOdj2w34Jdgno"
        },
        "href": "https://api.spotify.com/v1/tracks/1Q3TP11UOqOdj2w34Jdgno",
        "id": "1Q3TP11UOqOdj2w34Jdgno",
        "name": "Movement 9",
        "preview_url": null,
        "track_number": 9,
        "type": "track",
        "uri": "spotify:track:1Q3TP11UOqOdj2w34Jdgno",
        "is_local": false
      }
    ]
  },
  "copyrights": [
    {
      "text": "(C) 2021 Luaka Bop, Inc",
      "type": "C"
    },
    {
      "text": "(P) 2021 Luaka Bop, Inc",
      "type": "P"
    }
  ],
  "external_ids": {
    "upc": "680899009720"
  },
  "genres": [],
  "label": "Luaka Bop",
  "popularity": 39
}
'''


{
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
    "external_urls": {
        "spotify": "https://open.spotify.com/track/0QkT7SfXL9eR6tuQ7xb9ya"
    },
    "href": "https://api.spotify.com/v1/tracks/0QkT7SfXL9eR6tuQ7xb9ya",
    "id": "0QkT7SfXL9eR6tuQ7xb9ya",
    "name": "Movement 1",
    "preview_url": null,
    "track_number": 1,
    "type": "track",
    "uri": "spotify:track:0QkT7SfXL9eR6tuQ7xb9ya",
    "is_local": false
},
