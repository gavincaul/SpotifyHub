

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
        if self.data is None:
            self.data = self.get_playlist()
        return self.data["tracks"]["total"]

    def get_playlist_name(self):
        if self.data is None:
            self.data = self.get_playlist()
        return self.data["name"]

    def get_playlist_image(self):
        if self.data is None:
            self.data = self.get_playlist()
        try:
            return self.data["images"][0]["url"]
        except TypeError as e:
            print("ERROR: img is null {e}")
            return "https://static.thenounproject.com/png/3647578-200.png"
        
    def get_playlist_description(self):
        if self.data is None:
          self.data = self.get_playlist()
        return self.data["description"]
    
    def get_playlist_owner(self):
        if self.data is None:
            self.data = self.get_playlist()
        return (self.data["owner"]["id"], self.data["owner"]["display_name"])

    def get_playlist_follower_count(self):
        if self.data is None:
            self.data = self.get_playlist()
        return self.data["followers"]["total"]

    def get_playlist_visibility(self):
        if self.data is None:
            self.data = self.get_playlist()
        return self.data["public"]
    
    def get_playlist_tracks(self, total, positions=False):
        if self.data is None:
            self.data = self.get_playlist()

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
                if positions:
                    for i, item in enumerate(items):
                        songs.append((item, i+offset))
                else:
                    songs.extend(items)
                offset += len(items)

        return songs

    def get_playlist_track_names(self, total):
        tracks = self.get_playlist_tracks(total)
        track_list = []
        for item in tracks:
            track_list.append((item["track"]["id"], item["track"]["name"]))
        return track_list

    def get_playlist_track_names_and_positions(self, total):
        tracks = self.get_playlist_tracks(total, positions=True)
        track_list = []
        for item in tracks:
            track_list.append((item[0]["track"]["id"], (
                item[0]["track"]["name"], item[1])))
        return track_list



    def upload_cover_image(self, URL):
        try:
            if self.data is None:
                self.data = self.get_playlist()
            self.sp.playlist_upload_cover_image(self.playlist_id, URL)
            return True
        except Exception as e:
            print(f"WARNING. Upload_cover_image FAILED: {e}")
            return False

    def remove_specific_track(self, track_id, position, positions):
        # This function calls for the position to remove, and the positions to add.
        try:
            if self.data is None:
                self.data = self.get_playlist()
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
        try:
            if self.data is None:
                self.data = self.get_playlist()
            self.sp.playlist_remove_all_occurrences_of_items(
                self.playlist_id, items=[track_id])
            return True
        except Exception as e:
            print(f"WARNING. Adding track FAILED: {e}")
            return False

    def add_specific_tracks(self, track_id, position):
        try:
            if self.data is None:
                self.data = self.get_playlist()
            self.sp.playlist_add_items(self.playlist_id, [track_id], position)
            return True
        except Exception as e:
            print(f"WARNING. Adding track FAILED: {e}")
            return False
        
    def add_tracks(self, track_ids):
        try:
            if self.data is None:
              self.data=self.get_playlist()
            self.sp.playlist_add_items(self.playlist_id, items=track_ids)
            return True
        except Exception as e:
            print(f"WARNING. Failed to add tracks: {e}")
            return False
        
    def move_track(self, from_position, to_position):
        """Move a track within the playlist from one position to another."""
        try:
            if self.data is None:
                self.data = self.get_playlist()
            self.sp.playlist_reorder_items(
                self.playlist_id,
                range_start=from_position,
                insert_before=to_position
            )
            return True
        except Exception as e:
            print(f"WARNING. Failed to move track: {e}")
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
