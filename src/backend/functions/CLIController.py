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
                    parsed[flag] = value
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

            self.artist_cmds.get_artist_info(artist_id)

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
    # as - Artist Search

    # Track

    # s - Song details
    # ss - Save Song (liked songs)
    # spa - Song Playlist Add
    # spr - Song Playlist Remove
    # spl - Song Playlist List
    # su - Song Unsave
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
