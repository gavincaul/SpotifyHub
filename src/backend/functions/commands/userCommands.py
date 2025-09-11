from functions.models.user import User

class UserCommands:
    def __init__(self, spotify_manager):
        self.spotify_manager = spotify_manager

    user_list = {}

    def check_user(self, user_id=None):
        if user_id in self.user_list:
            return self.user_list[user_id]
    
        self.self.user_list[user_id] = User(self.spotify_manager, user_id=user_id)
        return self.user_list[user_id]