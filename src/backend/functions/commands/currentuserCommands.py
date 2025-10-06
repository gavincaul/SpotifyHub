from ..models.currentuser import CurrentUser
from ..database.currentUserManager import SettingsManager


class CurrentUserCommands:
    def __init__(self, spotify_manager):
        self.spotify_manager = spotify_manager
        self.current_user = None

    def cmd_login(self):
        """Login and set the current user"""
        if self.current_user is not None:
            print(f"Already logged in as {self.current_user.user_id}")
            return
        if self.spotify_manager.login_oauth():
            user_id = self.spotify_manager.get_current_user_id()
            if user_id:
                self.current_user = CurrentUser(self.spotify_manager)
                print(f"Logged in as {user_id}")
            else:
                print("Failed to get user info after login.")
        else:
            print("Login failed or cancelled.")

    def saved_albums_add(self, album_id=None, current_user=None):
        try:
            current_user.saved_albums([album_id])
            print("Album saved to your library")
        except Exception as e:
            print(f"Unable to save album: {e}")

    def create_user_playlist(self, playlist_name, description, public, collaborative, current_user=None):
        try:
            if description is None:
                description = ""
            if current_user is None:
                current_user = self.current_user
            return current_user.create_playlist(playlist_name, description, public, collaborative)
        except Exception as e:
            print(f"Unable to create playlist: {e}")

    def delete_user_playlist(self, playlist_id):
        return self.current_user.delete_playlist(playlist_id)
