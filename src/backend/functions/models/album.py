

class Album:
    def __init__(self, spotify_manager, album_id, data=None):
        self.sp = spotify_manager.get_spotify_client()
        self.data = data
        self.album_id = album_id
        self.spotify_manager = spotify_manager

    def get_album(self):
        if self.data is None:
            self.data = self.sp.album(self.album_id)
        return self.data

    def get_album_info(self):
        self.get_album()
        data = {
            "id": self.album_id,
            "name": self.get_album_name(),
            "artists": self.get_album_artist_ids(),
            "type": self.get_album_type(),
            "total": self.get_album_total_tracks(),
            "cover": self.get_album_cover(),
            "release_date": self.get_album_release_date(),
        }
        return data

    def get_album_name(self):
        self.get_album()
        return str(self.data.get("name", "Unknown Name"))

    def get_album_type(self):
        self.get_album()
        return str(self.data.get("type", "Unknown Type"))

    def get_album_total_tracks(self):
        self.get_album()
        return self.data.get("total_tracks", 0)

    def get_album_release_date(self):
        self.get_album()
        return str(self.data.get("release_date", "Unknown Release Date"))

    def get_album_cover(self):
        self.get_album()
        images = self.data.get("images") or []
        if images and len(images) > 0:
            return images[0].get("url", "https://static.thenounproject.com/png/3647578-200.png")
        return "https://static.thenounproject.com/png/3647578-200.png"

    def get_album_artist_ids(self):
        self.get_album()
        artists = self.data.get("artists") or []
        return [artist.get("id") for artist in artists if "id" in artist]

    def get_album_artist_data(self):
        self.get_album()
        artists = self.data.get("artists") or []
        return artists

    def get_album_artist_objects(self):
        from .artist import Artist
        self.get_album()
        artists = self.data.get("artists") or []
        return [
            Artist(spotify_manager=self.spotify_manager,
                   artist_id=artist.get("id"))
            for artist in artists if "id" in artist
        ]

    def get_album_tracks(self, positions=False):
        self.get_album()  # ensures self.data is populated
        tracks_data = self.data.get("tracks", {}).get("items", [])

        if positions:
            # Map track_number => track info
            track_dict = {}
            for t in tracks_data:
                track_dict[t["track_number"]] = {
                    "id": t.get("id"),
                    "name": t.get("name", "Unknown Name"),
                    "artists": [artist.get("name", "Unknown Artist") for artist in t.get("artists", [])],
                    "duration_ms": t.get("duration_ms"),
                    "href": t.get("external_urls", {}).get("spotify"),
                }
            return track_dict
        else:
            # Return a simple list
            track_list = []
            for t in tracks_data:
                track_list.append({
                    "id": t.get("id"),
                    "name": t.get("name", "Unknown Name"),
                    "artists": [artist.get("name", "Unknown Artist") for artist in t.get("artists", [])],
                    "duration_ms": t.get("duration_ms"),
                    "href": t.get("external_urls", {}).get("spotify"),
                    "track_number": t.get("track_number"),
                })
            return track_list


'''
{
  "album_type": "album",
  "total_tracks": 16,
  "external_urls": {
    "spotify": "https://open.spotify.com/album/3V18DIKvRuwdxc2LE4wuac"
  },
  "href": "https://api.spotify.com/v1/albums/3V18DIKvRuwdxc2LE4wuac?market=ES&locale=en-US%2Cen%3Bq%3D0.5",
  "id": "3V18DIKvRuwdxc2LE4wuac",
  "images": [
    {
      "url": "https://i.scdn.co/image/ab67616d0000b2736584177113cfae22014d3d90",
      "height": 640,
      "width": 640
    },
    {
      "url": "https://i.scdn.co/image/ab67616d00001e026584177113cfae22014d3d90",
      "height": 300,
      "width": 300
    },
    {
      "url": "https://i.scdn.co/image/ab67616d000048516584177113cfae22014d3d90",
      "height": 64,
      "width": 64
    }
  ],
  "name": "I Can Hear The Heart Beating As One",
  "release_date": "1997-04-22",
  "release_date_precision": "day",
  "type": "album",
  "uri": "spotify:album:3V18DIKvRuwdxc2LE4wuac",
  "artists": [
    {
      "external_urls": {
        "spotify": "https://open.spotify.com/artist/5hAhrnb0Ch4ODwWu4tsbpi"
      },
      "href": "https://api.spotify.com/v1/artists/5hAhrnb0Ch4ODwWu4tsbpi",
      "id": "5hAhrnb0Ch4ODwWu4tsbpi",
      "name": "Yo La Tengo",
      "type": "artist",
      "uri": "spotify:artist:5hAhrnb0Ch4ODwWu4tsbpi"
    }
  ],
  "tracks": {
    "href": "https://api.spotify.com/v1/albums/3V18DIKvRuwdxc2LE4wuac/tracks?offset=0&limit=50&market=ES&locale=en-US,en;q%3D0.5",
    "limit": 50,
    "next": null,
    "offset": 0,
    "previous": null,
    "total": 16,
    "items": [
      {
        "artists": [
          {
            "external_urls": {
              "spotify": "https://open.spotify.com/artist/5hAhrnb0Ch4ODwWu4tsbpi"
            },
            "href": "https://api.spotify.com/v1/artists/5hAhrnb0Ch4ODwWu4tsbpi",
            "id": "5hAhrnb0Ch4ODwWu4tsbpi",
            "name": "Yo La Tengo",
            "type": "artist",
            "uri": "spotify:artist:5hAhrnb0Ch4ODwWu4tsbpi"
          }
        ],
        "disc_number": 1,
        "duration_ms": 99733,
        "explicit": false,
        "external_urls": {
          "spotify": "https://open.spotify.com/track/488ciQxLvwIrBZbRXFud0A"
        },
        "href": "https://api.spotify.com/v1/tracks/488ciQxLvwIrBZbRXFud0A",
        "id": "488ciQxLvwIrBZbRXFud0A",
        "is_playable": true,
        "name": "Return to Hot Chicken",
        "preview_url": null,
        "track_number": 1,
        "type": "track",
        "uri": "spotify:track:488ciQxLvwIrBZbRXFud0A",
        "is_local": false
      },
      {
        "artists": [
          {
            "external_urls": {
              "spotify": "https://open.spotify.com/artist/5hAhrnb0Ch4ODwWu4tsbpi"
            },
            "href": "https://api.spotify.com/v1/artists/5hAhrnb0Ch4ODwWu4tsbpi",
            "id": "5hAhrnb0Ch4ODwWu4tsbpi",
            "name": "Yo La Tengo",
            "type": "artist",
            "uri": "spotify:artist:5hAhrnb0Ch4ODwWu4tsbpi"
          }
        ],
        "disc_number": 1,
        "duration_ms": 348693,
        "explicit": false,
        "external_urls": {
          "spotify": "https://open.spotify.com/track/00839RHIOqd7KUunk009jh"
        },
        "href": "https://api.spotify.com/v1/tracks/00839RHIOqd7KUunk009jh",
        "id": "00839RHIOqd7KUunk009jh",
        "is_playable": true,
        "name": "Moby Octopad",
        "preview_url": null,
        "track_number": 2,
        "type": "track",
        "uri": "spotify:track:00839RHIOqd7KUunk009jh",
        "is_local": false
      },
      {
        "artists": [
          {
            "external_urls": {
              "spotify": "https://open.spotify.com/artist/5hAhrnb0Ch4ODwWu4tsbpi"
            },
            "href": "https://api.spotify.com/v1/artists/5hAhrnb0Ch4ODwWu4tsbpi",
            "id": "5hAhrnb0Ch4ODwWu4tsbpi",
            "name": "Yo La Tengo",
            "type": "artist",
            "uri": "spotify:artist:5hAhrnb0Ch4ODwWu4tsbpi"
          }
        ],
        "disc_number": 1,
        "duration_ms": 201000,
        "explicit": false,
        "external_urls": {
          "spotify": "https://open.spotify.com/track/2nqaQ4WJ5tGTvGfQCvpBWT"
        },
        "href": "https://api.spotify.com/v1/tracks/2nqaQ4WJ5tGTvGfQCvpBWT",
        "id": "2nqaQ4WJ5tGTvGfQCvpBWT",
        "is_playable": true,
        "name": "Sugarcube",
        "preview_url": null,
        "track_number": 3,
        "type": "track",
        "uri": "spotify:track:2nqaQ4WJ5tGTvGfQCvpBWT",
        "is_local": false
      },
      {
        "artists": [
          {
            "external_urls": {
              "spotify": "https://open.spotify.com/artist/5hAhrnb0Ch4ODwWu4tsbpi"
            },
            "href": "https://api.spotify.com/v1/artists/5hAhrnb0Ch4ODwWu4tsbpi",
            "id": "5hAhrnb0Ch4ODwWu4tsbpi",
            "name": "Yo La Tengo",
            "type": "artist",
            "uri": "spotify:artist:5hAhrnb0Ch4ODwWu4tsbpi"
          }
        ],
        "disc_number": 1,
        "duration_ms": 279200,
        "explicit": false,
        "external_urls": {
          "spotify": "https://open.spotify.com/track/1VqZIPXYUxeW92lsWuJWB1"
        },
        "href": "https://api.spotify.com/v1/tracks/1VqZIPXYUxeW92lsWuJWB1",
        "id": "1VqZIPXYUxeW92lsWuJWB1",
        "is_playable": true,
        "name": "Damage",
        "preview_url": null,
        "track_number": 4,
        "type": "track",
        "uri": "spotify:track:1VqZIPXYUxeW92lsWuJWB1",
        "is_local": false
      },
      {
        "artists": [
          {
            "external_urls": {
              "spotify": "https://open.spotify.com/artist/5hAhrnb0Ch4ODwWu4tsbpi"
            },
            "href": "https://api.spotify.com/v1/artists/5hAhrnb0Ch4ODwWu4tsbpi",
            "id": "5hAhrnb0Ch4ODwWu4tsbpi",
            "name": "Yo La Tengo",
            "type": "artist",
            "uri": "spotify:artist:5hAhrnb0Ch4ODwWu4tsbpi"
          }
        ],
        "disc_number": 1,
        "duration_ms": 323133,
        "explicit": false,
        "external_urls": {
          "spotify": "https://open.spotify.com/track/07Be2TgmYSlJzI4aIA3m3n"
        },
        "href": "https://api.spotify.com/v1/tracks/07Be2TgmYSlJzI4aIA3m3n",
        "id": "07Be2TgmYSlJzI4aIA3m3n",
        "is_playable": true,
        "name": "Deeper into Movies",
        "preview_url": null,
        "track_number": 5,
        "type": "track",
        "uri": "spotify:track:07Be2TgmYSlJzI4aIA3m3n",
        "is_local": false
      },
      {
        "artists": [
          {
            "external_urls": {
              "spotify": "https://open.spotify.com/artist/5hAhrnb0Ch4ODwWu4tsbpi"
            },
            "href": "https://api.spotify.com/v1/artists/5hAhrnb0Ch4ODwWu4tsbpi",
            "id": "5hAhrnb0Ch4ODwWu4tsbpi",
            "name": "Yo La Tengo",
            "type": "artist",
            "uri": "spotify:artist:5hAhrnb0Ch4ODwWu4tsbpi"
          }
        ],
        "disc_number": 1,
        "duration_ms": 147040,
        "explicit": false,
        "external_urls": {
          "spotify": "https://open.spotify.com/track/6pKuJwQJH7ZoYIqBFIOUGD"
        },
        "href": "https://api.spotify.com/v1/tracks/6pKuJwQJH7ZoYIqBFIOUGD",
        "id": "6pKuJwQJH7ZoYIqBFIOUGD",
        "is_playable": true,
        "name": "Shadows",
        "preview_url": null,
        "track_number": 6,
        "type": "track",
        "uri": "spotify:track:6pKuJwQJH7ZoYIqBFIOUGD",
        "is_local": false
      },
      {
        "artists": [
          {
            "external_urls": {
              "spotify": "https://open.spotify.com/artist/5hAhrnb0Ch4ODwWu4tsbpi"
            },
            "href": "https://api.spotify.com/v1/artists/5hAhrnb0Ch4ODwWu4tsbpi",
            "id": "5hAhrnb0Ch4ODwWu4tsbpi",
            "name": "Yo La Tengo",
            "type": "artist",
            "uri": "spotify:artist:5hAhrnb0Ch4ODwWu4tsbpi"
          }
        ],
        "disc_number": 1,
        "duration_ms": 171093,
        "explicit": false,
        "external_urls": {
          "spotify": "https://open.spotify.com/track/2VcCu6ZIMVDYjINcygEuW2"
        },
        "href": "https://api.spotify.com/v1/tracks/2VcCu6ZIMVDYjINcygEuW2",
        "id": "2VcCu6ZIMVDYjINcygEuW2",
        "is_playable": true,
        "name": "Stockholm Syndrome",
        "preview_url": null,
        "track_number": 7,
        "type": "track",
        "uri": "spotify:track:2VcCu6ZIMVDYjINcygEuW2",
        "is_local": false
      },
      {
        "artists": [
          {
            "external_urls": {
              "spotify": "https://open.spotify.com/artist/5hAhrnb0Ch4ODwWu4tsbpi"
            },
            "href": "https://api.spotify.com/v1/artists/5hAhrnb0Ch4ODwWu4tsbpi",
            "id": "5hAhrnb0Ch4ODwWu4tsbpi",
            "name": "Yo La Tengo",
            "type": "artist",
            "uri": "spotify:artist:5hAhrnb0Ch4ODwWu4tsbpi"
          }
        ],
        "disc_number": 1,
        "duration_ms": 318373,
        "explicit": false,
        "external_urls": {
          "spotify": "https://open.spotify.com/track/19Qi2Cymjh7HDQESDrDBzs"
        },
        "href": "https://api.spotify.com/v1/tracks/19Qi2Cymjh7HDQESDrDBzs",
        "id": "19Qi2Cymjh7HDQESDrDBzs",
        "is_playable": true,
        "name": "Autumn Sweater",
        "preview_url": null,
        "track_number": 8,
        "type": "track",
        "uri": "spotify:track:19Qi2Cymjh7HDQESDrDBzs",
        "is_local": false
      },
      {
        "artists": [
          {
            "external_urls": {
              "spotify": "https://open.spotify.com/artist/5hAhrnb0Ch4ODwWu4tsbpi"
            },
            "href": "https://api.spotify.com/v1/artists/5hAhrnb0Ch4ODwWu4tsbpi",
            "id": "5hAhrnb0Ch4ODwWu4tsbpi",
            "name": "Yo La Tengo",
            "type": "artist",
            "uri": "spotify:artist:5hAhrnb0Ch4ODwWu4tsbpi"
          }
        ],
        "disc_number": 1,
        "duration_ms": 187093,
        "explicit": false,
        "external_urls": {
          "spotify": "https://open.spotify.com/track/35ZwXMhD8EIjko7CQAvDTy"
        },
        "href": "https://api.spotify.com/v1/tracks/35ZwXMhD8EIjko7CQAvDTy",
        "id": "35ZwXMhD8EIjko7CQAvDTy",
        "is_playable": true,
        "name": "Little Honda",
        "preview_url": null,
        "track_number": 9,
        "type": "track",
        "uri": "spotify:track:35ZwXMhD8EIjko7CQAvDTy",
        "is_local": false
      },
      {
        "artists": [
          {
            "external_urls": {
              "spotify": "https://open.spotify.com/artist/5hAhrnb0Ch4ODwWu4tsbpi"
            },
            "href": "https://api.spotify.com/v1/artists/5hAhrnb0Ch4ODwWu4tsbpi",
            "id": "5hAhrnb0Ch4ODwWu4tsbpi",
            "name": "Yo La Tengo",
            "type": "artist",
            "uri": "spotify:artist:5hAhrnb0Ch4ODwWu4tsbpi"
          }
        ],
        "disc_number": 1,
        "duration_ms": 343800,
        "explicit": false,
        "external_urls": {
          "spotify": "https://open.spotify.com/track/6o65Xn8X3IXf7zmxVjXDWJ"
        },
        "href": "https://api.spotify.com/v1/tracks/6o65Xn8X3IXf7zmxVjXDWJ",
        "id": "6o65Xn8X3IXf7zmxVjXDWJ",
        "is_playable": true,
        "name": "Green Arrow",
        "preview_url": null,
        "track_number": 10,
        "type": "track",
        "uri": "spotify:track:6o65Xn8X3IXf7zmxVjXDWJ",
        "is_local": false
      },
      {
        "artists": [
          {
            "external_urls": {
              "spotify": "https://open.spotify.com/artist/5hAhrnb0Ch4ODwWu4tsbpi"
            },
            "href": "https://api.spotify.com/v1/artists/5hAhrnb0Ch4ODwWu4tsbpi",
            "id": "5hAhrnb0Ch4ODwWu4tsbpi",
            "name": "Yo La Tengo",
            "type": "artist",
            "uri": "spotify:artist:5hAhrnb0Ch4ODwWu4tsbpi"
          }
        ],
        "disc_number": 1,
        "duration_ms": 145666,
        "explicit": false,
        "external_urls": {
          "spotify": "https://open.spotify.com/track/1L1hoK7nZXYUJzRA7yq8cz"
        },
        "href": "https://api.spotify.com/v1/tracks/1L1hoK7nZXYUJzRA7yq8cz",
        "id": "1L1hoK7nZXYUJzRA7yq8cz",
        "is_playable": true,
        "name": "One PM Again",
        "preview_url": null,
        "track_number": 11,
        "type": "track",
        "uri": "spotify:track:1L1hoK7nZXYUJzRA7yq8cz",
        "is_local": false
      },
      {
        "artists": [
          {
            "external_urls": {
              "spotify": "https://open.spotify.com/artist/5hAhrnb0Ch4ODwWu4tsbpi"
            },
            "href": "https://api.spotify.com/v1/artists/5hAhrnb0Ch4ODwWu4tsbpi",
            "id": "5hAhrnb0Ch4ODwWu4tsbpi",
            "name": "Yo La Tengo",
            "type": "artist",
            "uri": "spotify:artist:5hAhrnb0Ch4ODwWu4tsbpi"
          }
        ],
        "disc_number": 1,
        "duration_ms": 199266,
        "explicit": false,
        "external_urls": {
          "spotify": "https://open.spotify.com/track/5akjusKRK2fyA1iY6DTNQH"
        },
        "href": "https://api.spotify.com/v1/tracks/5akjusKRK2fyA1iY6DTNQH",
        "id": "5akjusKRK2fyA1iY6DTNQH",
        "is_playable": true,
        "name": "The Lie and How We Told It",
        "preview_url": null,
        "track_number": 12,
        "type": "track",
        "uri": "spotify:track:5akjusKRK2fyA1iY6DTNQH",
        "is_local": false
      },
      {
        "artists": [
          {
            "external_urls": {
              "spotify": "https://open.spotify.com/artist/5hAhrnb0Ch4ODwWu4tsbpi"
            },
            "href": "https://api.spotify.com/v1/artists/5hAhrnb0Ch4ODwWu4tsbpi",
            "id": "5hAhrnb0Ch4ODwWu4tsbpi",
            "name": "Yo La Tengo",
            "type": "artist",
            "uri": "spotify:artist:5hAhrnb0Ch4ODwWu4tsbpi"
          }
        ],
        "disc_number": 1,
        "duration_ms": 162306,
        "explicit": false,
        "external_urls": {
          "spotify": "https://open.spotify.com/track/6bBobm1wePzB1WG7FD68zd"
        },
        "href": "https://api.spotify.com/v1/tracks/6bBobm1wePzB1WG7FD68zd",
        "id": "6bBobm1wePzB1WG7FD68zd",
        "is_playable": true,
        "name": "Center of Gravity",
        "preview_url": null,
        "track_number": 13,
        "type": "track",
        "uri": "spotify:track:6bBobm1wePzB1WG7FD68zd",
        "is_local": false
      },
      {
        "artists": [
          {
            "external_urls": {
              "spotify": "https://open.spotify.com/artist/5hAhrnb0Ch4ODwWu4tsbpi"
            },
            "href": "https://api.spotify.com/v1/artists/5hAhrnb0Ch4ODwWu4tsbpi",
            "id": "5hAhrnb0Ch4ODwWu4tsbpi",
            "name": "Yo La Tengo",
            "type": "artist",
            "uri": "spotify:artist:5hAhrnb0Ch4ODwWu4tsbpi"
          }
        ],
        "disc_number": 1,
        "duration_ms": 640560,
        "explicit": false,
        "external_urls": {
          "spotify": "https://open.spotify.com/track/3KOHHNFGzkRWdKFSHVFjHv"
        },
        "href": "https://api.spotify.com/v1/tracks/3KOHHNFGzkRWdKFSHVFjHv",
        "id": "3KOHHNFGzkRWdKFSHVFjHv",
        "is_playable": true,
        "name": "Spec Bebop",
        "preview_url": null,
        "track_number": 14,
        "type": "track",
        "uri": "spotify:track:3KOHHNFGzkRWdKFSHVFjHv",
        "is_local": false
      },
      {
        "artists": [
          {
            "external_urls": {
              "spotify": "https://open.spotify.com/artist/5hAhrnb0Ch4ODwWu4tsbpi"
            },
            "href": "https://api.spotify.com/v1/artists/5hAhrnb0Ch4ODwWu4tsbpi",
            "id": "5hAhrnb0Ch4ODwWu4tsbpi",
            "name": "Yo La Tengo",
            "type": "artist",
            "uri": "spotify:artist:5hAhrnb0Ch4ODwWu4tsbpi"
          }
        ],
        "disc_number": 1,
        "duration_ms": 385466,
        "explicit": false,
        "external_urls": {
          "spotify": "https://open.spotify.com/track/2RCaDbgmfL6xge4jEZYwV6"
        },
        "href": "https://api.spotify.com/v1/tracks/2RCaDbgmfL6xge4jEZYwV6",
        "id": "2RCaDbgmfL6xge4jEZYwV6",
        "is_playable": true,
        "name": "We're an American Band",
        "preview_url": null,
        "track_number": 15,
        "type": "track",
        "uri": "spotify:track:2RCaDbgmfL6xge4jEZYwV6",
        "is_local": false
      },
      {
        "artists": [
          {
            "external_urls": {
              "spotify": "https://open.spotify.com/artist/5hAhrnb0Ch4ODwWu4tsbpi"
            },
            "href": "https://api.spotify.com/v1/artists/5hAhrnb0Ch4ODwWu4tsbpi",
            "id": "5hAhrnb0Ch4ODwWu4tsbpi",
            "name": "Yo La Tengo",
            "type": "artist",
            "uri": "spotify:artist:5hAhrnb0Ch4ODwWu4tsbpi"
          }
        ],
        "disc_number": 1,
        "duration_ms": 145573,
        "explicit": false,
        "external_urls": {
          "spotify": "https://open.spotify.com/track/2bY66Hf5NbHJ8Ai8eNmJHG"
        },
        "href": "https://api.spotify.com/v1/tracks/2bY66Hf5NbHJ8Ai8eNmJHG",
        "id": "2bY66Hf5NbHJ8Ai8eNmJHG",
        "is_playable": true,
        "name": "My Little Corner of the World",
        "preview_url": null,
        "track_number": 16,
        "type": "track",
        "uri": "spotify:track:2bY66Hf5NbHJ8Ai8eNmJHG",
        "is_local": false
      }
    ]
  },
  "copyrights": [
    {
      "text": "1997 Matador Records",
      "type": "C"
    },
    {
      "text": "1997 Matador Records",
      "type": "P"
    }
  ],
  "external_ids": {
    "upc": "744861022237"
  },
  "genres": [],
  "label": "Matador",
  "popularity": 51,
  "is_playable": true
}
'''
