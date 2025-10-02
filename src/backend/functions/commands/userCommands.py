from functions.models.user import User

class UserCommands:
    def __init__(self, spotify_manager):
        self.spotify_manager = spotify_manager
        self.user_cache = {}

    def check_user(self, user_id=None):
        if user_id in self.user_cache:
            return self.user_cache[user_id]
    
        self.self.user_cache[user_id] = User(self.spotify_manager, user_id=user_id)
        return self.user_cache[user_id]
    

    def check_exists(self, user_id):
        if user_id in self.user_cache:
            return True
        try:
            data = self.spotify_manager.sp.user(user_id)
            user_obj = User(self.spotify_manager, user_id, data=data)
            self.user_cache[user_id] = user_obj
            return True
        except self.spotify_manager.sp.exceptions.SpotifyException as e:
            return e.http_status not in [400, 404]