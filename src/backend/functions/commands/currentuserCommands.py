from functions.models.currentuser import CurrentUser

class CurrentUserCommands:
    def __init__(self, spotify_manager):
        self.spotify_manager = spotify_manager


    def cmd_login(self):
        """Login and set the current user"""
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
            current_user.sp.current_user.saved_albums([album_id])
            print("Album saved to your library")
        except Exception as e:
            print(f"Unable to save album: {e}")

