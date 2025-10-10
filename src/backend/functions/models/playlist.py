from ...utils.utils import missing_file_url


class Playlist:
    def __init__(self, spotify_manager, playlist_id, data=None):
        self.sp = spotify_manager.get_spotify_client()
        self.data = data
        self.playlist_id = playlist_id
        self.spotify_manager = spotify_manager

    def get_playlist(self):
        if self.data is None:
            self.data = self.sp.playlist(self.playlist_id)
        return self.data

    def get_playlist_length(self):
        self.get_playlist()
        return self.data["tracks"]["total"]

    def get_playlist_name(self):
        self.get_playlist()

        return self.data["name"]

    def get_playlist_image(self):
        self.get_playlist()

        try:
            return self.data["images"][0]["url"]
        except TypeError as e:
            print("ERROR: img is null {e}")
            return missing_file_url

    def get_playlist_description(self):
        self.get_playlist()

        return self.data["description"]

    def get_playlist_owner(self):
        self.get_playlist()

        return (self.data["owner"]["id"], self.data["owner"]["display_name"])

    def get_playlist_url(self):
        self.get_playlist()

        return self.data["external_urls"].get("spotify", "")

    def get_playlist_follower_count(self):
        self.get_playlist()

        return self.data["followers"]["total"]

    def get_playlist_visibility(self):
        self.get_playlist()

        return self.data["public"]

    def get_playlist_collaborative(self):
        self.get_playlist()

        return self.data["collaborative"]

    def get_playlist_tracks(self, total, positions=False):
        self.get_playlist()

        songs = []
        limit = 50
        offset = 0

        if total is None:
            self.get_playlist_length()

        else:
            while len(songs) < total:
                result = self.sp.playlist_tracks(self.playlist_id,
                                                 limit=min(limit, total - offset), offset=offset)
                items = result["items"]
                if not items:
                    break
                else:
                    songs.extend(items)
                offset += len(items)

        return songs

    def get_playlist_tracks_info(self, total):
        tracks = self.get_playlist_tracks(total)
        track_list = []
        for i, item in enumerate(tracks):
            track = item["track"]
            if track is not None:
              track_info = {
                  "id": track["id"],
                  "name": track["name"],
                  "artist_data": [{"name": artist["name"], "id": artist["id"]} for artist in track["artists"]],
                  "album_data": {"name": track["album"]["name"], "id": track["album"]["id"], "images": {"large": track["album"]["images"][0]["url"] if len(track["album"]["images"]) > 0 else missing_file_url, "medium": track["album"]["images"][1]["url"] if len(track["album"]["images"]) > 1 else missing_file_url, "small": track["album"]["images"][2]["url"] if len(track["album"]["images"]) > 2 else missing_file_url}},
                  "duration_ms": track["duration_ms"],
                  "position": i+1,
                  "explicit": track["explicit"],
                  "popularity": track["popularity"],
                  "added_at": item["added_at"],
                  "added_by": item["added_by"]["id"] if item["added_by"] else None,
                  "is_local": item["is_local"],
                  "url": track["external_urls"].get("spotify", "")
              }
              track_list.append(track_info)
            else:
                print(item)
        return track_list

    def get_playlist_track_ids(self, total):
        tracks = self.get_playlist_tracks(total)
        track_list = [item["track"]["id"] for item in tracks]
        return track_list

    def upload_cover_image_raw(self, image_b64):
        self.get_playlist()
        try:
            self.sp.playlist_upload_cover_image(self.playlist_id, image_b64)
            return True
        except Exception as e:
            print(f"WARNING. Upload_cover_image FAILED: {e}")
            return False

    def remove_specific_track(self, track_id, position, positions):
        # This function calls for the position to remove, and the positions to add.
        self.get_playlist()

        try:
            self.sp.playlist_remove_specific_occurrences_of_items(
                self.playlist_id, items=[{"uri": f"spotify:track:{track_id}", "positions": [position]}])
            for p in positions:
                if position != p - 1:
                    # If the removed track is lower than the position, this prevents OutOfBounds err
                    x = 1 if p - 1 < position else 2
                    self.add_specific_tracks(track_id=track_id, position=p-x)
            return True
        except Exception as e:
            print(f"WARNING. Adding track FAILED: {e}")
            return False

    def remove_tracks(self, track_id):
        self.get_playlist()

        try:
            self.sp.playlist_remove_all_occurrences_of_items(
                self.playlist_id, items=[track_id])
            return True
        except Exception as e:
            print(f"WARNING. Adding track FAILED: {e}")
            return False

    def add_specific_tracks(self, track_id, position):
        self.get_playlist()
        pll = self.get_playlist_length()
        if position>pll-1:
            position=pll
        try:

            self.sp.playlist_add_items(self.playlist_id, track_id, position)
            return True
        except Exception as e:
            print(f"WARNING. Adding track FAILED: {e}")
            return False

    def add_tracks(self, track_ids):
        self.get_playlist()

        try:
            self.sp.playlist_add_items(self.playlist_id, items=track_ids)
            return True
        except Exception as e:
            print(f"WARNING. Failed to add tracks: {e}")
            raise e

    def move_tracks(self, from_positions, to_position):
        """
        Move one or more tracks within the playlist.
        from_positions: list of integers (track indices to move)
        to_position: integer (target insert position)
        """
        self.get_playlist()

        # Ensure positions are sorted so you move in a stable order
        from_positions = sorted(set(from_positions))
        try:
            # Since the list shifts after each move, adjust positions to the front, then
            for offset, pos in enumerate(from_positions):
                
                adjusted_from = pos
                adjusted_to = 0 + offset
                sanity = self.sp.playlist_reorder_items(
                    self.playlist_id,
                    range_start=adjusted_from,
                    insert_before=adjusted_to,
                    range_length=1
                )
                if "snapshot_id" not in sanity:
                    print(f"WARNING. Failed to move track at pos {pos} to {to_position}")
                    return False
            mtl = len(from_positions) #move track length

            sanity = self.sp.playlist_reorder_items(
                    self.playlist_id,
                    range_start=0,
                    insert_before=to_position,
                    range_length=mtl
                )
            if "snapshot_id" not in sanity:
                print(f"WARNING. Failed to move track at pos {pos} to {to_position}")
                return False
            return True
        except Exception as e:
            print(f"WARNING. Failed to move tracks: {e}")
            return False


'''
{
  "collaborative": false,
  "description": "",
  "external_urls": {
    "spotify": "https://open.spotify.com/playlist/2VIEwbtYHIQZvDAtflRnHM"
  },
  "href": "https://api.spotify.com/v1/playlists/2VIEwbtYHIQZvDAtflRnHM?market=ES&locale=en-US%2Cen%3Bq%3D0.5",
  "id": "2VIEwbtYHIQZvDAtflRnHM",
  "images": [
    {
      "url": "https://i.scdn.co/image/ab67616d00001e02eab40fc794b88b9d1e012578",
      "height": null,
      "width": null
    }
  ],
  "name": "Rap",
  "owner": {
    "external_urls": {
      "spotify": "https://open.spotify.com/user/9yiidfk1ydpewq4u1ge28fidh"
    },
    "href": "https://api.spotify.com/v1/users/9yiidfk1ydpewq4u1ge28fidh",
    "id": "9yiidfk1ydpewq4u1ge28fidh",
    "type": "user",
    "uri": "spotify:user:9yiidfk1ydpewq4u1ge28fidh",
    "display_name": "gavin caulfield"
  },
  "public": true,
  "snapshot_id": "AAAAAu2IHo8pdr0txc0ui0ESL8HHNkPh",
  "tracks": {
    "href": "https://api.spotify.com/v1/playlists/2VIEwbtYHIQZvDAtflRnHM/tracks?offset=0&limit=100&market=ES&locale=en-US,en;q%3D0.5",
    "limit": 100,
    "next": null,
    "offset": 0,
    "previous": null,
    "total": 1,
    "items": [
      {
        "added_at": "2021-01-12T01:11:18Z",
        "added_by": {
          "external_urls": {
            "spotify": "https://open.spotify.com/user/9yiidfk1ydpewq4u1ge28fidh"
          },
          "href": "https://api.spotify.com/v1/users/9yiidfk1ydpewq4u1ge28fidh",
          "id": "9yiidfk1ydpewq4u1ge28fidh",
          "type": "user",
          "uri": "spotify:user:9yiidfk1ydpewq4u1ge28fidh"
        },
        "is_local": false,
        "track": {
          "album": {
            "album_type": "compilation",
            "total_tracks": 24,
            "external_urls": {
              "spotify": "https://open.spotify.com/album/5qENHeCSlwWpEzb25peRmQ"
            },
            "href": "https://api.spotify.com/v1/albums/5qENHeCSlwWpEzb25peRmQ",
            "id": "5qENHeCSlwWpEzb25peRmQ",
            "images": [
              {
                "url": "https://i.scdn.co/image/ab67616d0000b273eab40fc794b88b9d1e012578",
                "height": 640,
                "width": 640
              },
              {
                "url": "https://i.scdn.co/image/ab67616d00001e02eab40fc794b88b9d1e012578",
                "height": 300,
                "width": 300
              },
              {
                "url": "https://i.scdn.co/image/ab67616d00004851eab40fc794b88b9d1e012578",
                "height": 64,
                "width": 64
              }
            ],
            "name": "Curtain Call: The Hits (Deluxe Edition)",
            "release_date": "2005-12-06",
            "release_date_precision": "day",
            "type": "album",
            "uri": "spotify:album:5qENHeCSlwWpEzb25peRmQ",
            "artists": [
              {
                "external_urls": {
                  "spotify": "https://open.spotify.com/artist/7dGJo4pcD2V6oG8kP0tJRR"
                },
                "href": "https://api.spotify.com/v1/artists/7dGJo4pcD2V6oG8kP0tJRR",
                "id": "7dGJo4pcD2V6oG8kP0tJRR",
                "name": "Eminem",
                "type": "artist",
                "uri": "spotify:artist:7dGJo4pcD2V6oG8kP0tJRR"
              }
            ],
            "is_playable": true
          },
          "artists": [
            {
              "external_urls": {
                "spotify": "https://open.spotify.com/artist/7dGJo4pcD2V6oG8kP0tJRR"
              },
              "href": "https://api.spotify.com/v1/artists/7dGJo4pcD2V6oG8kP0tJRR",
              "id": "7dGJo4pcD2V6oG8kP0tJRR",
              "name": "Eminem",
              "type": "artist",
              "uri": "spotify:artist:7dGJo4pcD2V6oG8kP0tJRR"
            }
          ],
          "disc_number": 1,
          "duration_ms": 326466,
          "explicit": true,
          "external_ids": {
            "isrc": "USIR10211559"
          },
          "external_urls": {
            "spotify": "https://open.spotify.com/track/5Z01UMMf7V1o0MzF86s6WJ"
          },
          "href": "https://api.spotify.com/v1/tracks/5Z01UMMf7V1o0MzF86s6WJ",
          "id": "5Z01UMMf7V1o0MzF86s6WJ",
          "is_playable": true,
          "name": "Lose Yourself",
          "popularity": 77,
          "preview_url": null,
          "track_number": 6,
          "type": "track",
          "uri": "spotify:track:5Z01UMMf7V1o0MzF86s6WJ",
          "is_local": false,
          "episode": false,
          "track": true
        },
        "primary_color": null,
        "video_thumbnail": {
          "url": null
        }
      }
    ]
  },
  "type": "playlist",
  "uri": "spotify:playlist:2VIEwbtYHIQZvDAtflRnHM",
  "followers": {
    "href": null,
    "total": 0
  },
  "primary_color": null
}
'''
