import os
from pathlib import Path
from dotenv import load_dotenv
import spotipy
from spotipy.oauth2 import SpotifyOAuth, SpotifyClientCredentials
from ..utils.redis_client import redis_client


class SpotifyManager:
    def __init__(self, client_id=None, client_secret=None, redirect_uri=None, scope=None):
        BASE_DIR = Path(__file__).resolve().parent.parent.parent.parent
        load_dotenv(BASE_DIR / "config/.env")

        self.client_id = client_id or os.getenv("SPOTIFY_CLIENT_ID")
        self.client_secret = client_secret or os.getenv(
            "SPOTIFY_CLIENT_SECRET")
        self.redirect_uri = redirect_uri or os.getenv("SPOTIFY_REDIRECT_URI")
        self.scope = scope or os.getenv("SPOTIFY_SCOPE")
        self.redis_client = redis_client
        # Public client (non-user requests)
        self.sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(
            client_id=self.client_id,
            client_secret=self.client_secret
        ))

        self.sp_oauth = SpotifyOAuth(
            client_id=self.client_id,
            client_secret=self.client_secret,
            redirect_uri=self.redirect_uri,
            scope=self.scope
        )
        self.current_user_id = None

    def _create_oauth(self,):

        self.sp_oauth = SpotifyOAuth(
            client_id=self.client_id,
            client_secret=self.client_secret,
            redirect_uri=self.redirect_uri,
            scope=self.scope,

        )
        return

    def get_auth_url(self, user_id=None):
        if self.sp_oauth is None:
            self._create_oauth(user_id)
        return self.sp_oauth.get_authorize_url()

    def login_with_code(self, code: str, debug:bool = False):

        if not self.sp_oauth:
            raise Exception("OAuth not initialized. Call get_auth_url first.")
        if debug:
            print("accessing Token")
        token_info = self.sp_oauth.get_access_token(code)
        if debug:
            print("Completed ACcess Token")
        access_token = token_info["access_token"]
        refresh_token = token_info["refresh_token"]
        if self.sp:
            self.sp.__del__()
        # Use user-specific client
        if debug:
            print("Creating SP")
        self.sp = spotipy.Spotify(auth=access_token)
        if debug:
            print("Getting UID")
        self.current_user_id = self.get_current_user_id()
        if debug:
            print("Setting Redis")
        self.redis_client.set(
            f"spotify_user:{self.current_user_id}", refresh_token)
        return self.current_user_id

    def logout(self):
        """Clear Spotify session and remove cached token from Redis"""

        if self.current_user_id:
            self.redis_client.delete(f"spotify_user:{self.current_user_id}")
            self.current_user_id = None

        # Reset Spotify client to public credentials
        if self.sp:
            self.sp.__del__()
        self.sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(
            client_id=self.client_id,
            client_secret=self.client_secret
        ))

    def get_spotify_client(self):
        return self.sp

    def get_current_user_id(self):
        try:
            user = self.sp.current_user()
            return user["id"]
        except spotipy.exceptions.SpotifyException:
            return None
