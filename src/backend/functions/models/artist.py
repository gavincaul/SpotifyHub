class Artist:
    def __init__(self, spotify_manager, artist_id, data=None):
        self.sp = spotify_manager.get_spotify_client()
        self.data = data
        self.artist_id = artist_id
        self.spotify_manager = spotify_manager

    def get_artist(self):
        if self.data == None:
            self.data = self.sp.artist(self.artist_id)
        return self.data

    def get_artist_info(self):
        self.get_artist()
        data = {
            "id": self.artist_id,
            "url": self.get_artist_url(),
            "name": self.get_artist_name(),
            "genres": self.get_artist_genres(),
            "popularity": self.get_artist_popularity(),
            "followers": self.get_artist_followers(),
            "imageURL": self.get_artist_image(),
        }
        return data

    def get_artist_name(self):
        self.get_artist()

        return self.data["name"]

    def get_artists(self, artist_ids):
        self.get_artist()

        if artist_ids == None or len(artist_ids) == 0:
            return []
        if len(artist_ids) > 50:
            raise ValueError("Maximum of 50 artist IDs allowed")
        if len(artist_ids) == 1:
            return [self.sp.artist(artist_ids[0])]
        return self.sp.artists(artist_ids)["artists"]

    def get_artist_url(self):
        self.get_artist()
        return self.data["external_urls"].get("spotify", "https://www.open.spotify.com/artist/" + self.artist_id)

    def get_artist_genres(self):
        self.get_artist()

        return self.data["genres"]

    def get_artist_popularity(self):
        self.get_artist()

        return self.data["popularity"]

    def get_artist_followers(self):
        self.get_artist()

        return self.data["followers"]["total"]

    def get_artist_id(self):
        return self.artist_id

    def get_artist_image(self):
        self.get_artist()
        images = self.data.get("images") or []
        if images and len(images) > 0:
            return images[0].get("url", "https://static.thenounproject.com/png/3647578-200.png")
        return "https://static.thenounproject.com/png/3647578-200.png"

    def get_artist_top_tracks(self, country="US", raw=False):
        self.get_artist()

        tracks = self.sp.artist_top_tracks(
            self.artist_id, country=country)["tracks"]
        if raw:
            return tracks
        track_list = []
        for t in tracks:
            track_list.append({"name": t.get("name", "Unknown Name"), "artists": [
                              a.get("name", "Unknown Artist") for a in t["artists"]],
                "popularity": t.get("popularity", "Unknown Popularity"),
                "id": t.get("id", "Unknown ID")})
        return track_list

    def get_artist_albums(self, include_groups=None, limit=20, offset=0):
        self.get_artist()
        if include_groups is None:
            include_groups = ["album", "single", "appears_on", "compilation"]
        include_groups_str = ",".join(include_groups)
        albums = self.sp.artist_albums(
            self.artist_id, include_groups=include_groups_str, limit=limit, offset=offset)["items"]
        album_list = []
        for a in albums:
            album_list.append({"type": a.get("album_type"), "group": a.get("album_group"), "name": a.get("name", "Unknown Name"), "artists": [
                              t.get("name", "Unknown Artist") for t in a["artists"]], "url": a["external_urls"].get("spotify", "Unknown URL"),
                "imageURL": a["images"][0].get("url", "https://static.thenounproject.com/png/3647578-200.png"), })
        return album_list


'''
{
  "external_urls": {
    "spotify": "https://open.spotify.com/artist/5Z3IWpvwOvoaWodujHw7xh"
  },
  "followers": {
    "href": null,
    "total": 130482
  },
  "genres": [],
  "href": "https://api.spotify.com/v1/artists/5Z3IWpvwOvoaWodujHw7xh?locale=en-US%2Cen%3Bq%3D0.5",
  "id": "5Z3IWpvwOvoaWodujHw7xh",
  "images": [
    {
      "url": "https://i.scdn.co/image/ab6761610000e5ebbe862dadd4231c1735bb452a",
      "height": 640,
      "width": 640
    },
    {
      "url": "https://i.scdn.co/image/ab67616100005174be862dadd4231c1735bb452a",
      "height": 320,
      "width": 320
    },
    {
      "url": "https://i.scdn.co/image/ab6761610000f178be862dadd4231c1735bb452a",
      "height": 160,
      "width": 160
    }
  ],
  "name": "Dan Deacon",
  "popularity": 41,
  "type": "artist",
  "uri": "spotify:artist:5Z3IWpvwOvoaWodujHw7xh"
}
'''
