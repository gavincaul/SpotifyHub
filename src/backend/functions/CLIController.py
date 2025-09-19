from functions.commands import playlistCommands, userCommands, songCommands, albumCommands, currentuserCommands, artistCommands
from functions import spotifymanager


class CLIController:
    def __init__(self):
        self.spotify_manager = spotifymanager.SpotifyManager(
            scope="user-library-read user-read-private user-follow-read playlist-modify-public user-top-read user-library-modify user-follow-modify"
        )
        self.current_user = None
        self.album_cmds = albumCommands.AlbumCommands(self.spotify_manager)
        self.playlist_cmds = playlistCommands.PlaylistCommands(
            self.spotify_manager)
        self.song_cmds = songCommands.SongCommands(self.spotify_manager)
        self.user_cmds = userCommands.UserCommands(self.spotify_manager)
        self.currentuser_cmds = currentuserCommands.CurrentUserCommands(
            self.spotify_manager)
        self.artist_cmds = artistCommands.ArtistCommands(self.spotify_manager)

        # Define all flags and their expected type
        self.flags = {
            "-a": {"requires_value": False},
            "--all": {"requires_value": False},
            "-n": {"requires_value": True, "type": int},
            "--num": {"requires_value": True, "type": int},
            "-v": {"requires_value": True, "type": str},
            "--val": {"requires_value": True, "type": str},
            "-p": {"requires_value": True, "type": str},
            "--playlist": {"requires_value": True, "type": str},
        }

    def arg_parser(self, args: list):
        """Parse flags into a clean dictionary of {flag: value}."""
        parsed = {}
        i = 0
        while i < len(args):
            flag = args[i]
            if flag not in self.flags:
                print(f"Unknown argument: {flag}")
                i += 1
                continue

            flag_info = self.flags[flag]
            if flag_info["requires_value"]:
                if i + 1 >= len(args):
                    print(f"Flag {flag} requires a value but none given")
                    parsed[flag] = None
                else:
                    raw_value = args[i + 1]
                    try:
                        value = flag_info.get("type", str)(raw_value)
                    except ValueError:
                        print(f"Invalid type for flag {flag}: {raw_value}")
                        value = None
                    parsed[flag] = self.strip_URL(value)
                    i += 1  # skip the value
            else:
                parsed[flag] = True
            i += 1
        return parsed

    def cmd_login(self, *args):
        """Login and set the current user"""
        self.currentuser_cmds.cmd_login()
        # Update CLIController's current_user reference
        self.current_user = self.currentuser_cmds.current_user

    def check_string(self, s):
        return (isinstance(s, str) and s.strip() != "")

    def strip_URL(self, s):
        if not self.check_string(s):
            return s
        if "spotify.com" in s:
            parts = s.split("/")
            if len(parts) > 0:
                last_part = parts[-1]
                if "?" in last_part:
                    last_part = last_part.split("?")[0]
                return last_part
        return s.strip()

    def prompt_time_range(self):
        time_range_map = {"s": "short_term",
                          "m": "medium_term", "l": "long_term"}
        descriptions = {"s": "short term: 4 weeks",
                        "m": "medium term: 6 months", "l": "long term: ~1 year"}

        while True:
            print("Time range options:")
            for key, desc in descriptions.items():
                print(f"  {key}: {desc}")
            selection = input(
                "Please select a time range (s/m/l) or 'q' to cancel: ").strip().lower()

            if selection == "q":
                print("Cancelling command with no execution")
                return None
            if selection in time_range_map:
                return time_range_map[selection]

            print("Invalid input. Please try again.")

    # Album
    # b - Get Album
    def cmd_b(self, *args):
        """Returns Album Information (-v <ALBUM>)"""
        try:
            args_dict = self.arg_parser(args)
            album_id = args_dict.get(
                "-v") or self.strip_URL(input("Enter Album ID: "))

            self.album_cmds.get_album_info(album_id)

        except Exception as e:
            print(f"Error retrieving album info: {e}")

    # bl - Album (track) list

    def cmd_bl(self, *args):
        """Returns Album Track List (-v <ALBUM>)"""
        try:
            args_dict = self.arg_parser(args)
            album_id = args_dict.get(
                "-v") or self.strip_URL(input("Enter Album ID: "))

            tracks = self.album_cmds.track_list(album_id)
            for t in tracks:
                print(self.song_cmds.get_song_info(t.track_id))

        except Exception as e:
            print(f"Error retrieving album track list: {e}")
    # ba - Album Artist

    def cmd_ba(self, *args):
        """Returns Album Artists (-v <ALBUM>)"""
        try:
            args_dict = self.arg_parser(args)
            album_id = args_dict.get(
                "-v") or self.strip_URL(input("Enter Album ID: "))

            artists = self.album_cmds.get_album_artists(album_id)
            for artist in artists:
                print(self.artist_cmds.get_artist_info(artist.artist_id))

        except Exception as e:
            print(f"Error retrieving album artists: {e}")

    # bs - Album Save
    def cmd_bs(self, *args):
        """Saves Album to Your Library (-v <ALBUM>)"""
        try:
            if not self.current_user:
                print("You must login first")
                return

            args_dict = self.arg_parser(args)
            album_id = args_dict.get(
                "-v") or self.strip_URL(input("Enter Album ID: "))

            self.album_cmds.save(album_id, self.current_user)

        except Exception as e:
            print(f"Error saving album: {e}")

    # bsu - Album Unsave
    def cmd_bsu(self, *args):
        """Removes Album from Your Library (-v <ALBUM>)"""
        try:
            if not self.current_user:
                print("You must login first")
                return

            args_dict = self.arg_parser(args)
            album_id = args_dict.get(
                "-v") or self.strip_URL(input("Enter Album ID: "))

            self.album_cmds.unsave(album_id, self.current_user)

        except Exception as e:
            print(f"Error removing album: {e}")

    # Artist

    # a - Artist details
    def cmd_a(self, *args):
        """Returns Artist Information (-v <ARTIST>)"""
        try:
            args_dict = self.arg_parser(args)
            artist_id = args_dict.get(
                "-v") or self.strip_URL(input("Enter Artist ID: "))

            artist_obj = self.artist_cmds.get_artist_info(artist_id)
            print(f"Name: {artist_obj.get_artist_name()}")
            print(f"Genres: {', '.join(artist_obj.get_artist_genres())}")
            print(f"Followers: {artist_obj.get_artist_followers()}")
            print(f"Popularity: {artist_obj.get_artist_popularity()}")
            print(f"Image URL: {artist_obj.get_artist_image_url()}")
        except Exception as e:
            print(f"Error retrieving artist info: {e}")

    # at - Artist Top Tracks -v
    def cmd_at(self, *args):
        """Returns Artist Top Tracks (-v <ARTIST>)"""
        try:
            args_dict = self.arg_parser(args)
            artist_id = args_dict.get(
                "-v") or self.strip_URL(input("Enter Artist ID: "))

            tracks = self.artist_cmds.top_tracks(artist_id)
            for t in tracks:
                print(self.song_cmds.get_song_info(t.track_id))

        except Exception as e:
            print(f"Error retrieving artist top tracks: {e}")

    # aa - Artist Top Albums

    def cmd_aa(self, *args):
        """Returns Artist Top Albums (-v <ARTIST>)"""
        try:
            args_dict = self.arg_parser(args)
            artist_id = args_dict.get(
                "-v") or self.strip_URL(input("Enter Artist ID: "))

            albums = self.artist_cmds.top_albums(artist_id)

            for album in albums:
                print(self.album_cmds.get_album_info(album_id=album.album_id))

        except Exception as e:
            print(f"Error retrieving artist top albums: {e}")

    # ar - Artist Related
    '''Depreceated due to API limitations'''

    # ap - Artist Song's on Playlist
    def cmd_ap(self, *args):
        """Returns Artist's Songs on a Playlist (-v <ARTIST> -p <PLAYLIST>)"""
        try:
            args_dict = self.arg_parser(args)
            artist_id = args_dict.get(
                "-v") or self.strip_URL(input("Enter Artist ID: "))
            playlist_id = args_dict.get(
                "-p") or self.strip_URL(input("Enter Playlist ID: "))

            tracks = self.artist_cmds.playlist_tracks(artist_id, playlist_id)
            for t in tracks:
                print(self.song_cmds.get_song_info(t.track_id))

        except Exception as e:
            print(f"Error retrieving artist songs on playlist: {e}")

    # apc - Create Artist Playlist
    # apcp - Create Artist Playlist from Playlist (splice)
    # atg - Artist Genres
    def cmd_atg(self, *args):
        """Returns Artist's Genres (-v <ARTIST> -p <PLAYLIST>)"""
        try:
            args_dict = self.arg_parser(args)
            artist_id = args_dict.get(
                "-v") or self.strip_URL(input("Enter Artist ID: "))
            genres = self.artist_cmds.get_artist_genres(artist_id)
            print("Artist Genres")
            for i, g in enumerate(genres):
                print(f"({i}) {g}")
        except Exception as e:
            print(f"Error retrieving artist genres: {e}")
    # as - Artist Search

    def cmd_as(self, *args):
        """Returns List of Artists from search (-v <ARTIST SEARCH VALUE>)"""
        try:
            args_dict = self.arg_parser(args)
            search_value = args_dict.get(
                "-v") or self.strip_URL(input("Enter Search Value: "))
            search = self.artist_cmds.search_artist(
                search_value)  # [[artist_name, id], ...]
            print("Possible Artists")

            for i, a in enumerate(search):
                print(f"({i}) {a[0]}, ID: {a[1]}")
        except Exception as e:
            print(f"Error searching for artist(s): {e}")

    # Track

    # s - Song details
    def cmd_s(self, *args):
        """Returns Track Information (-v <TRACK_ID>)"""
        try:
            args_dict = self.arg_parser(args)
            track_id = args_dict.get(
                "-v") or self.strip_URL(input("Enter Track ID: "))
            song_obj = self.song_cmds.get_song_info(track_id)
            print(f"Song Name: {song_obj.get_track_name()}")
            print(
                f"Artists: {', '.join([artist.get_artist_name() for artist in song_obj.get_track_artists()])}")
            print(f"Album: {song_obj.get_track_album().get_album_name()}")
            print(f"Duration (ms): {song_obj.get_track_length_ms()}")
            print(f"Popularity: {song_obj.get_track_popularity()}")
            print(f"Explicit: {song_obj.is_track_explicit()}")
            print(f"External URL: {song_obj.get_track_url()}")

        except Exception as e:
            print(f"Error retrieving artist info: {e}")

    # ss - Save Song (liked songs)
    def cmd_ss(self, *args):
        """Saves song to 'Liked Songs' (-v <TRACK_ID)"""
        try:
            if not self.current_user:
                print("You must login first")
                return
            args_dict = self.arg_parser(args)
            track_id = args_dict.get(
                "-v") or self.strip_URL(input("Enter Track ID: "))
            self.song_cmds.save_song(track_id, self.current_user)
        except Exception as e:
            print(f"Error saving song: {e}")
    # sus - Song Unsave (liked songs)

    def cmd_sus(self, *args):
        """Unsaves song from 'Liked Songs' (-v <TRACK_ID)"""
        try:
            if not self.current_user:
                print("You must login first")
                return
            args_dict = self.arg_parser(args)
            track_id = args_dict.get(
                "-v") or self.strip_URL(input("Enter Track ID: "))
            self.song_cmds.unsave_song(track_id, self.current_user)
        except Exception as e:
            print(f"Error unsaving song: {e}")

    # spa - Song Playlist Add

    def cmd_spa(self, *args):
        """Adds song to playlist (-v <TRACK_ID> -p <PLAYLIST>)"""
        try:
            if not self.current_user:
                print("You must login first")
                return
            args_dict = self.arg_parser(args)
            track_id = args_dict.get(
                "-v") or self.strip_URL(input("Enter Track ID: "))
            playlist_id = args_dict.get(
                "-p") or self.strip_URL(input("Enter Playlist ID: "))
            self.song_cmds.add_song_to_playlist(
                track_id, playlist_id, current_user=self.current_user)
            print("Added song(s) to playlist")
        except Exception as e:
            print(f"Error adding song to playlist: {e}")

        # spr - Song Playlist Remove
    def cmd_spr(self, *args):
        """Removes song from playlist (-v <TRACK_ID> -p <PLAYLIST>)"""
        try:
            if not self.current_user:
                print("You must login first")
                return
            args_dict = self.arg_parser(args)
            track_id = args_dict.get(
                "-v") or self.strip_URL(input("Enter Track ID: "))
            playlist_id = args_dict.get(
                "-p") or self.strip_URL(input("Enter Playlist ID: "))
            self.song_cmds.remove_song_from_playlist(
                track_id, playlist_id, current_user=self.current_user)
            print("Removed song(s) to playlist")
        except Exception as e:
            print(f"Error removing song from playlist: {e}")
        # spl - Song Playlist List

    def cmd_spl(self, *args):
        """Lists whether or not a song is on a playlist (-v <TRACK_ID> -p <PLAYLIST>)"""
        try:
            args_dict = self.arg_parser(args)
            track_id = args_dict.get(
                "-v") or self.strip_URL(input("Enter Track ID: "))
            playlist_id = args_dict.get(
                "-p") or self.strip_URL(input("Enter Playlist ID: "))
            print("Getting playlist tracks...")
            playlist_tracks = self.playlist_cmds.get_playlist_track_names(
                playlist_id)
            print("Sifting for song...")
            result = self.song_cmds.check_song_on_playlist(
                track_id, playlist_tracks)
            if result != "":
                print(f"Song {result} found on playlist")
            else:
                print(f"Song not found on playlist")
        except Exception as e:
            print(f"Error finding song on playlist: {e}")

        # sl - Song List

        # Playlist

        # p - playlist details
        # ptl - playlist track list
        # ptx - playlist track exchange (replace)
        # ppi - playlist playlist intersection
        # ppu - playlist playlist union
        # pc - playlist create
        # pimg - playlist image
        # pimgr - playlist image replace
        # pd - delete playlist
        # ptm - playlist track move
        # pdd - playlist details description
        # pdn - playlist details name
        # pdp - playlist details public
        # pti - playlist track(s) insert
        # pti - playlist track(s) insert (in) spot (-s)
        # ptd - playlist track delete

        # User

        # u - Return User Information
        # ulf - User List FollowerS
        # ulfg - User List FollowinG
        # ulp - User List Playlists (-a, -n, -v)
        # ultt - User List Top Tracks (-n, -a)
        # ulta - User List Top Artists (-n, -a)
        # ufp - User follow playlist (-v)
        # ufpu - User UNfollow playlist (-v)
        # us - User Save Song (-v)
        # usu - User Unsave Song (-v)
        # usb - User Saved Albums
