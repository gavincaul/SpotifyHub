


import json
import pprint
import spotipy
import spotipy.util as util
from spotipy.oauth2 import SpotifyOAuth
CLIENT_SECRET = '6195378b5b3a45a68ff3eace3196d038'
CLIENT_ID = '14572a826f7e4b8f9e724ef61beb60a8'
REDIRECT_URI = 'http://localhost:8888'
USERNAME = 'gavincaulfield' #9yiidfk1ydpewq4u1ge28fidh
SCOPE = 'playlist-modify-public'

"""

FUNCTION: getToken

Retrieves refreshed token from Spotify API

@params: None

@returns: api token

"""

def getToken():
	try:
		sp_oauth = SpotifyOAuth(CLIENT_ID, CLIENT_SECRET, REDIRECT_URI, scope=SCOPE, username=USERNAME)
		token_info = sp_oauth.get_cached_token()

		if token_info and sp_oauth.is_token_expired(token_info):
			refresh_token = token_info["refresh_token"]
			new_token_info = sp_oauth.refresh_access_token(refresh_token)
			return new_token_info["access_token"]

		return sp_oauth.get_access_token(code=None, as_dict=False)
	except spotipy.oauth2.SpotifyOauthError as e:
		print(f"Error with spotipy OAuth: {e}")
		return None

TOKEN = getToken()
sp = spotipy.Spotify(auth=getToken())



def getPlaylist(playlist_id, token=TOKEN):

    if token is None:
        print("Error: Access token is not available.")
        return None

    try:
        playlist = sp.playlist(playlist_id)
        return playlist
    except spotipy.SpotifyException as e:
        print(f"Error with spotipy: {e}")
        return None