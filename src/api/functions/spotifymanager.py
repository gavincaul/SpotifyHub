import spotipy
from spotipy.oauth2 import SpotifyOAuth
from dotenv import load_dotenv
import os
from src.api.functions.user import User




class SpotifyManager:
    def __init__(self, client_id=None, client_secret=None, redirect_uri=None, scope=None, username=None):
        load_dotenv(dotenv_path="/home/gavin/VSC/SpotifyProjects/Current/SpotifyHub/config/.env")
        self.scope = scope
        self.client_id = client_id or os.getenv("SPOTIFY_CLIENT_ID")
        self.client_secret = client_secret or os.getenv("SPOTIFY_CLIENT_SECRET")
        self.redirect_uri = redirect_uri or os.getenv("SPOTIFY_REDIRECT_URI")
        self.username = username

        self.sp = spotipy.Spotify(auth=self.getToken())
    def getToken(self):
        try:
            sp_oauth = SpotifyOAuth(self.client_id, self.client_secret, self.redirect_uri, scope=self.scope)
            token_info = sp_oauth.get_cached_token()

            if token_info and sp_oauth.is_token_expired(token_info):
                refresh_token = token_info["refresh_token"]
                new_token_info = sp_oauth.refresh_access_token(refresh_token)
                return new_token_info["access_token"]

            return sp_oauth.get_access_token(code=None, as_dict=False)
        except spotipy.oauth2.SpotifyOauthError as e:
            print(f"Error with spotipy OAuth: {e}")
            return None



    def get_spotify_client(self):
        return self.sp
    

    def get_user(self):
        return User(self, user_id=self.username)




