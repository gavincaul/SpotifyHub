from .user import User
from functions.database.currentUserManager import SettingsManager


class CurrentUser(User):
    def __init__(self, spotify_manager, data=None):
        user_id = spotify_manager.get_current_user_id()
        self.data = data
        if not user_id:
            raise ValueError("Unable to fetch current user ID.")
        super().__init__(spotify_manager, user_id)
        self.user_settings = SettingsManager(
            user_id=self.user_id, current_user=self)


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

        self.user_settings.set(key="properties/" + setting, value=value, default=default)
        


    def get_user_top_tracks(self, total=None, time_range="medium_term"):
        if self.data is None:
            self.data = self.sp.current_user()

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
        if self.data is None:
            self.data = self.sp.current_user()

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
        if self.data is None:
            self.data = self.sp.current_user()
        try:
            self.sp.current_user_follow_playlist(playlist_id)
            print(f"Successfully followed playlist")
        except Exception as e:
            print(f"Failed to follow playlist: {e}")

    def unfollow_playlist(self, playlist_id):
        if self.data is None:
            self.data = self.sp.current_user()
        try:
            self.sp.current_user_unfollow_playlist(playlist_id)
            print(f"Successfully unfollowed playlist")
        except Exception as e:
            print(f"Failed to follow playlist: {e}")

    def get_user_following(self, total=None):
        if self.data is None:
            self.data = self.sp.current_user()

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
        if self.data is None:
            self.data = self.sp.current_user()
        try:
            self.sp.current_user_saved_albums_add(album_ids)
        except Exception as e:
            print(f"Unable to save albums: {e}")

    def saved_albums_remove(self, album_ids):
        if self.data is None:
            self.data = self.sp.current_user()
        try:
            self.sp.current_user_saved_albums_delete(album_ids)
        except Exception as e:
            print(f"Unable to save albums: {e}")

    def saved_tracks_add(self, track_ids):
        if self.data is None:
            self.data = self.sp.current_user()
        try:
            self.sp.current_user_saved_tracks_add(track_ids)
        except Exception as e:
            print(f"Unable to save track(s): {e}")

    def saved_tracks_delete(self, track_ids):
        if self.data is None:
            self.data = self.sp.current_user()
        try:
            self.sp.current_user_saved_tracks_delete(track_ids)
        except Exception as e:
            print(f"Unable to unsave track(s): {e}")

    def playlist_add_items(self, track_id, playlist_id, position=None):
        if self.data is None:
            self.data = self.sp.current_user()
        try:
            self.sp.playlist_add_items(
                playlist_id, [track_id], position)
        except Exception as e:
            print(f"Unable to add track(s) to playlist: {e}")

    def playlist_remove_items(self, track_id, playlist_id, position=None):
        if self.data is None:
            self.data = self.sp.current_user()
        try:
            self.sp.playlist_remove_all_occurrences_of_items(
                playlist_id, [track_id], position)
        except Exception as e:
            print(f"Unable to add track(s) to playlist: {e}")

    def create_playlist(self, playlist_name, description, public, collaborative):
        if self.data is None:
            self.data = self.sp.current_user()
        result = self.sp.user_playlist_create(self.user_id, playlist_name, public, collaborative, description)
        return result["id"]
    
    def delete_playlist(self, playlist_id):
        if self.data is None:
            self.data = self.sp.current_user()
        self.sp.current_user_unfollow_playlist(playlist_id)
        return True

    '''
    
    '''
