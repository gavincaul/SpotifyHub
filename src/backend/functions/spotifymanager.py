import spotipy
from spotipy.oauth2 import SpotifyOAuth
from dotenv import load_dotenv
import os
from pathlib import Path


class SpotifyManager:
    def __init__(self, client_id=None, client_secret=None, redirect_uri=None, scope=None):

        BASE_DIR = Path(__file__).resolve().parent.parent.parent.parent
        load_dotenv(BASE_DIR / "config/.env")
        self.scope = scope
        self.client_id = client_id or os.getenv("SPOTIFY_CLIENT_ID")
        self.client_secret = client_secret or os.getenv(
            "SPOTIFY_CLIENT_SECRET")
        self.redirect_uri = redirect_uri or os.getenv("SPOTIFY_REDIRECT_URI")

        self.sp_oauth = SpotifyOAuth(
            client_id=self.client_id,
            client_secret=self.client_secret,
            redirect_uri=self.redirect_uri,
            scope=self.scope,
            cache_path=".cache"  # token cache file (can customize per user)
        )
        self.sp = None  # will hold spotipy.Spotify client after login

    def login_oauth(self):
        """Starts the OAuth flow to login user and get token."""
        token_info = self.sp_oauth.get_cached_token()
        if not token_info:
            # No cached token, ask user to login
            auth_url = self.sp_oauth.get_authorize_url()
            print(f"Please navigate here and authorize: {auth_url}")
            response = input("Paste the redirected URL here: ").strip()

            code = self.sp_oauth.parse_response_code(response)
            if code:
                token_info = self.sp_oauth.get_access_token(code)
            else:
                print("Invalid response URL, login failed.")
                return False

        access_token = token_info['access_token']
        self.sp = spotipy.Spotify(auth=access_token)
        return True

    def get_spotify_client(self):
        if not self.sp:
            # If no login, fallback to client credentials (public data only)
            self.sp = spotipy.Spotify(auth_manager=spotipy.SpotifyClientCredentials(
                client_id=self.client_id,
                client_secret=self.client_secret
            ))
        return self.sp

    def get_current_user_id(self):
        if not self.sp:
            self.get_spotify_client()
        try:
            user = self.sp.current_user()
            return user['id']
        except spotipy.exceptions.SpotifyException:
            return None

    def get_user_profile(self, uid):
        if not self.sp:
            self.get_spotify_client()
        if not uid:
            print("Invalid User ID")
            return -1
        try:
            user = self.sp.user(uid)
            return user
        except spotipy.exceptions.SpotifyException as e:
            print(f"Insufficient User ID. {e.msg}.")
            return -1
        



