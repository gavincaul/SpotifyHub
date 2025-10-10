from .user import User
from ....database.currentUserManager import SettingsManager
from ...utils.utils import missing_file_url


class CurrentUser(User):
    def __init__(self, spotify_manager, data=None):
        user_id = spotify_manager.get_current_user_id()
        self.data = data
        if not user_id:
            raise ValueError("Unable to fetch current user ID.")
        super().__init__(spotify_manager, user_id)
        self.user_settings = SettingsManager(
            user_id=self.user_id, current_user=self)
        self.playlists = None

    def get_user_settings(self):
        if self.user_settings is None:
            self.user_settings = SettingsManager(
                user_id=self.user_id, current_user=self)
        return self.user_settings.settings

    def get_specific_user_settings(self, setting, default=None):
        if self.user_settings is None:
            self.user_settings = SettingsManager(
                user_id=self.user_id, current_user=self)

        return self.user_settings.get(key="properties/" + setting, default=default)

    def set_specific_user_settings(self, setting, value, default=None):
        if self.user_settings is None:
            self.user_settings = SettingsManager(
                user_id=self.user_id, current_user=self)

        self.user_settings.set(key="properties/" + setting,
                               value=value, default=default)

    def get_user_profile(self):
        if self.data is None:
            self.data = self.sp.current_user()

        return self.data

    def get_user_top_tracks(self, total: int = None, time_range="medium_term"):
        self.get_user_profile()

        top_tracks = []
        limit = 50
        offset = 0

        if total is None:
            result = self.sp.current_user_top_tracks(
                limit=limit, offset=offset, time_range=time_range)
            total = result["total"]
            top_tracks.extend(result["items"])
            offset += len(result["items"])
        else:
            print(type(total))
            while len(top_tracks) < total:
                result = self.sp.current_user_top_tracks(
                    limit=min(limit, total - offset), offset=offset, time_range=time_range)
                items = result["items"]
                if not items:
                    break
                top_tracks.extend(items)
                offset += len(items)

        return top_tracks

    def get_user_top_artists(self, total=None, time_range="medium_term"):
        self.get_user_profile()

        top_artists = []
        limit = 50
        offset = 0

        if total is None:
            result = self.sp.current_user_top_artists(
                limit=limit, offset=offset, time_range=time_range)
            total = result["total"]
            top_artists.extend(result["items"])
            offset += len(result["items"])
        else:
            while len(top_artists) < total:
                result = self.sp.current_user_top_artists(
                    limit=min(limit, total - offset), offset=offset, time_range=time_range)
                items = result["items"]
                if not items:
                    break
                top_artists.extend(items)
                offset += len(items)

        return top_artists

    def follow_playlist(self, playlist_id):
        self.get_user_profile()

        try:
            self.sp.current_user_follow_playlist(playlist_id)
            print(f"Successfully followed playlist")
        except Exception as e:
            print(f"Failed to follow playlist: {e}")

    def unfollow_playlist(self, playlist_id):
        self.get_user_profile()

        try:
            self.sp.current_user_unfollow_playlist(playlist_id)
            print(f"Successfully unfollowed playlist")
        except Exception as e:
            print(f"Failed to follow playlist: {e}")

    def get_user_following(self, total=None):
        self.get_user_profile()

        following = []
        limit = 50
        after = None
        fetched = 0

        while True:
            remaining = total - fetched if total else limit
            fetch_limit = min(limit, remaining)

            result = self.sp.current_user_followed_artists(
                limit=fetch_limit, after=after)
            artists = result["artists"]["items"]
            following.extend(artists)

            fetched += len(artists)

            if len(artists) < fetch_limit:
                break

            after = artists[-1]["id"]

            if total and fetched >= total:
                break

        return following

    def saved_albums_add(self, album_ids):
        self.get_user_profile()

        try:
            self.sp.current_user_saved_albums_add(album_ids)
        except Exception as e:
            print(f"Unable to save albums: {e}")

    def saved_albums_delete(self, album_ids):
        self.get_user_profile()

        try:
            self.sp.current_user_saved_albums_delete(album_ids)
        except Exception as e:
            print(f"Unable to save albums: {e}")

    def saved_tracks_add(self, track_ids):
        self.get_user_profile()

        try:
            self.sp.current_user_saved_tracks_add(track_ids)
        except Exception as e:
            print(f"Unable to save track(s): {e}")

    def saved_tracks_delete(self, track_ids):
        self.get_user_profile()

        try:
            self.sp.current_user_saved_tracks_delete(track_ids)
        except Exception as e:
            print(f"Unable to unsave track(s): {e}")

    def playlist_add_items(self, track_id, playlist_id, position=None):
        self.get_user_profile()

        try:
            self.sp.playlist_add_items(
                playlist_id, [track_id], position)
        except Exception as e:
            print(f"Unable to add track(s) to playlist: {e}")

    def playlist_remove_items(self, track_id, playlist_id, position=None):
        self.get_user_profile()

        try:
            self.sp.playlist_remove_all_occurrences_of_items(
                playlist_id, [track_id], position)
        except Exception as e:
            print(f"Unable to add track(s) to playlist: {e}")

    def create_playlist(self, playlist_name, description, public, collaborative):
        self.get_user_profile()

        result = self.sp.user_playlist_create(
            self.user_id, playlist_name, public, collaborative, description)
        return result["id"]

    def delete_playlist(self, playlist_id):
        self.get_user_profile()
        try:
            self.sp.current_user_unfollow_playlist(playlist_id)
            print(f"Successfully unfollowed playlist")
        except Exception as e:
            print(f"Failed to follow playlist: {e}")

    def unfollow_user(self, user_id):
        self.get_user_profile()

        try:
            self.sp.user_unfollow_users(user_id)
        except Exception as e:
            print(f"Unable to unfollow user: {e}")

    def follow_user(self, user_id):
        self.get_user_profile()

        try:
            self.sp.user_follow_users(user_id)
        except Exception as e:
            print(f"Unable to follow user: {e}")

    def unfollow_artist(self, artist_id):
        self.get_user_profile()

        try:
            self.sp.user_unfollow_artists(artist_id)
        except Exception as e:
            print(f"Unable to unfollow artist: {e}")

    def follow_artist(self, artist_id):
        self.get_user_profile()

        try:
            self.sp.user_follow_artists(artist_id)
        except Exception as e:
            print(f"Unable to follow artist: {e}")

    def get_user_devices(self):
        self.get_user_profile()

        try:
            devices = self.sp.devices()
            return devices.get("devices", [])
        except Exception as e:
            print(f"Unable to get user devices: {e}")
            return []

    def get_user_playlists(self, total=None):
        """Fetch current user's playlists from Spotify"""
        # Ensure self.playlists always exists
        if not hasattr(self, "playlists") or self.playlists is None:
            self.playlists = []

        playlists = []  # local variable

        offset = 0
        fetched = 0

        # Fetch total if not provided
        if total is None:
            first_batch = self.sp.current_user_playlists(limit=50)
            total = first_batch.get("total", 0)

        while fetched < total:
            limit = min(50, total - fetched)
            user_playlists = self.sp.current_user_playlists(
                limit=limit, offset=offset)

            items = user_playlists.get("items", [])
            for playlist in items:
                playlists.append({
                    "name": playlist.get("name", "Unknown Name"),
                    "ownerName": playlist.get("owner", {}).get("display_name", "Unknown Owner"),
                    "ownerID": playlist.get("owner", {}).get("id", "Unknown Id"),
                    "id": playlist.get("id", "Unknown Id"),
                    "public": playlist.get("public", True),
                    "collaborative": playlist.get("collaborative", False),
                    "length": playlist.get("tracks", {}).get("total", 0),
                    "description": playlist.get("description", ""),
                    "url": playlist.get("external_urls", {}).get("spotify", ""),
                    "coverURL": playlist.get("images")[0]["url"] if playlist.get("images") else missing_file_url
                })

            fetched += len(items)
            offset += limit
            if len(items) < limit:
                break

        # Save playlists to instance for caching
        self.playlists = playlists

        return self.playlists

    def get_user_albums(self, total=None):
        """Fetch current user's saved albums from Spotify"""
        if not hasattr(self, "albums") or self.albums is None:
            self.albums = []

        albums = []
        offset = 0
        fetched = 0

        # Fetch total if not provided
        if total is None:
            first_batch = self.sp.current_user_saved_albums(limit=50)
            total = first_batch.get("total", 0)

        while fetched < total:
            limit = min(50, total - fetched)
            user_albums = self.sp.current_user_saved_albums(
                limit=limit, offset=offset)

            items = user_albums.get("items", [])
            for item in items:
                if item is not None:
                    album = item.get("album", {})
                    albums.append({
                        "id": album.get("id", "Unknown Id"),
                        "name": album.get("name", "Unknown Album"),
                        "artists": [{"id": a.get("id", ""), "name": a.get("name", "")} for a in album.get("artists", [])],
                        "genres": album.get("genres", []),
                        "release_date": album.get("release_date", ""),
                        "total_tracks": album.get("total_tracks", 0),
                        "url": album.get("external_urls", {}).get("spotify", ""),
                        "images": {"small": album["images"][2].get("url", "") if album["images"] else missing_file_url, "medium": album["images"][1].get("url", "") if album["images"] else missing_file_url, "large": album["images"][0].get("url", "") if album["images"] else missing_file_url}
                    })

            fetched += len(items)
            offset += limit
            if len(items) < limit:
                break

        self.albums = albums
        return self.albums

    def get_user_tracks(self, total=None):
        """Fetch current user's saved tracks from Spotify"""
        if not hasattr(self, "tracks") or self.tracks is None:
            self.tracks = []

        tracks = []
        offset = 0
        fetched = 0

        if total is None:
            first_batch = self.sp.current_user_saved_tracks(limit=50)
            total = first_batch.get("total", 0)

        while fetched < total:
            limit = min(50, total - fetched)
            user_tracks = self.sp.current_user_saved_tracks(
                limit=limit, offset=offset)

            items = user_tracks.get("items", [])
            for item in items:
                if item is not None:
                    track = item.get("track", {})
                    tracks.append({
                        "id": track["id"],
                        "name": track["name"],
                        "artist_data": [{"name": artist["name"], "id": artist["id"]} for artist in track["artists"]],
                        "album_data": {"name": track["album"]["name"], "id": track["album"]["id"], "images": {"large": track["album"]["images"][0]["url"] if len(track["album"]["images"]) > 0 else missing_file_url, "medium": track["album"]["images"][1]["url"] if len(track["album"]["images"]) > 1 else missing_file_url, "small": track["album"]["images"][2]["url"] if len(track["album"]["images"]) > 2 else missing_file_url}},
                        "duration_ms": track["duration_ms"],
                        "explicit": track["explicit"],
                        "popularity": track["popularity"],
                        "added_at": item["added_at"],
                        "url": track["external_urls"].get("spotify", "")
                    })

            fetched += len(items)
            offset += limit
            if len(items) < limit:
                break

        self.tracks = tracks
        return self.tracks

    def get_user_artists(self, total=None):
        """Fetch current user's followed artists from Spotify"""
        if not hasattr(self, "artists") or self.artists is None:
            self.artists = []

        artists = []
        after = None
        fetched = 0

        # The Spotify API for followed artists is a bit different (uses `after` instead of `offset`)
        while True:
            results = self.sp.current_user_followed_artists(
                limit=50, after=after)
            artist_items = results.get("artists", {}).get("items", [])

            for artist in artist_items:
                if artist is not None and artist != {}:
                    artists.append({
                        "id": artist.get("id", "Unknown Id"),
                        "name": artist.get("name", "Unknown Artist"),
                        "genres": artist.get("genres", []),
                        "followers": artist.get("followers", {}).get("total", 0),
                        "url": artist.get("external_urls", {}).get("spotify", ""),
                        "images": {"small": artist["images"][2].get("url", "") if artist["images"] else missing_file_url, "medium": artist["images"][1].get("url", "") if artist["images"] else missing_file_url, "large": artist["images"][0].get("url", "") if artist["images"] else missing_file_url}
                    })
            fetched += len(artist_items)
            if len(artist_items) < 50:
                break  # No more artists

            after = artist_items[-1].get("id")

        self.artists = artists
        return self.artists

    '''
    {
  "country": "US",
  "display_name": "gavin caulfield",
  "email": "coolies0617@aol.com",
  "explicit_content": {
    "filter_enabled": false,
    "filter_locked": false
  },
  "external_urls": {
    "spotify": "https://open.spotify.com/user/9yiidfk1ydpewq4u1ge28fidh"
  },
  "followers": {
    "href": null,
    "total": 50
  },
  "href": "https://api.spotify.com/v1/users/9yiidfk1ydpewq4u1ge28fidh",
  "id": "9yiidfk1ydpewq4u1ge28fidh",
  "images": [
    {
      "url": "https://i.scdn.co/image/ab6775700000ee85d0cbc08494544d02f6bd9e2a",
      "height": 300,
      "width": 300
    },
    {
      "url": "https://i.scdn.co/image/ab67757000003b82d0cbc08494544d02f6bd9e2a",
      "height": 64,
      "width": 64
    }
  ],
  "product": "premium",
  "type": "user",
  "uri": "spotify:user:9yiidfk1ydpewq4u1ge28fidh"
}
    '''
