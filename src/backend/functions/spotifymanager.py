import spotipy
from spotipy.oauth2 import SpotifyOAuth, SpotifyClientCredentials
from dotenv import load_dotenv
import os
from pathlib import Path
from spotipy.cache_handler import RedisCacheHandler
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
        # Default public client
        self.sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(
            client_id=self.client_id,
            client_secret=self.client_secret
        ))
        cache_handler = RedisCacheHandler(
            self.redis_client,
        )
        self.current_user_id = None
        self.sp_oauth = SpotifyOAuth(
            client_id=self.client_id,
            client_secret=self.client_secret,
            redirect_uri=self.redirect_uri,
            scope=self.scope,
            cache_handler=cache_handler
        )
        self.user_cache_handler = None

    def _create_oauth(self, user_id=None):
        """Create SpotifyOAuth with Redis caching per user"""
        key = f"spotify_token:{user_id}" if user_id else None
        if key:
            self.current_user_id = user_id
        cache_handler = RedisCacheHandler(self.redis_client, key=key)
        self.sp_oauth = SpotifyOAuth(
            client_id=self.client_id,
            client_secret=self.client_secret,
            redirect_uri=self.redirect_uri,
            scope=self.scope,
            cache_handler=cache_handler
        )
        self.user_cache_handler = cache_handler

    def get_auth_url(self, user_id=None):
        self._create_oauth(user_id)
        return self.sp_oauth.get_authorize_url()

    def login_with_code(self, code: str):
        if not self.sp_oauth:
            raise Exception("OAuth not initialized. Call get_auth_url first.")
        token_info = self.sp_oauth.get_access_token(code)
        access_token = token_info["access_token"]

        # Use user-specific client
        self.sp = spotipy.Spotify(auth=access_token)
        self.current_user_id = self.get_current_user_id()

        return self.current_user_id

    def logout(self):
        """Clear Spotify session and remove cached token from Redis"""
        # Reset Spotify client to public credentials
        self.sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(
            client_id=self.client_id,
            client_secret=self.client_secret
        ))
        # Delete token from Redis if cached
        if self.user_cache_handler and self.current_user_id:
            try:
                self.redis_client.delete(
                    f"spotify_token:{self.current_user_id}")
                print(f"✅ Deleted Redis token for {self.current_user_id}")
            except Exception as e:
                print(f"⚠️ Failed to delete Redis token: {e}")

        # Clear OAuth and user info
        self.current_user_id = None
        self.user_cache_handler = None
        self.sp_oauth = None

    def get_spotify_client(self):
        return self.sp

    def get_current_user_id(self):
        try:
            user = self.sp.current_user()
            return user["id"]
        except spotipy.exceptions.SpotifyException:
            return None
