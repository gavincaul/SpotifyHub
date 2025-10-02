

class User:
    def __init__(self, spotify_manager, user_id, data=None):
        self.sp = spotify_manager.get_spotify_client()
        self.spotify_manager = spotify_manager
        self.data = data
        self.playlists = []
        self.user_id = user_id

    def get_user_profile(self):
        if self.data is None:
            self.data = self.sp.user(self.user_id)
        return self.data
    
    def get_user_playlists(self, total=None):
        from .playlist import Playlist
        if not self.playlists:
            offset = 0
            fetched = 0

        
            if not total:
                first_batch = self.sp.user_playlists(self.user_id, limit=50)
                total = first_batch["total"]

            while fetched < total:
                limit = min(50, total - fetched)
                user_playlists = self.sp.user_playlists(self.user_id, limit=limit, offset=offset)

                for playlist in user_playlists["items"]:
                    self.playlists.append(
                        Playlist(spotify_manager=self.spotify_manager, playlist_id=playlist["id"])
                    )

                fetched += len(user_playlists["items"])
                offset += limit

                if len(user_playlists["items"]) < limit:
                    break  

        return self.playlists
    
    
'''
{
  "display_name": "gavin caulfield",
  "external_urls": {
    "spotify": "https://open.spotify.com/user/9yiidfk1ydpewq4u1ge28fidh"
  },
  "followers": {
    "href": null,
    "total": 50
  },
  "href": "https://api.spotify.com/v1/users/9yiidfk1ydpewq4u1ge28fidh",
  "id": "9yiidfk1ydpewq4u1ge28fidh",
  "images": [
    {
      "url": "https://i.scdn.co/image/ab6775700000ee85d0cbc08494544d02f6bd9e2a",
      "height": 300,
      "width": 300
    },
    {
      "url": "https://i.scdn.co/image/ab67757000003b82d0cbc08494544d02f6bd9e2a",
      "height": 64,
      "width": 64
    }
  ],
  "type": "user",
  "uri": "spotify:user:9yiidfk1ydpewq4u1ge28fidh"
}
'''
    