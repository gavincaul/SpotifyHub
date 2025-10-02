import base64
import uuid

import requests
from functions.commands import playlistCommands, userCommands, songCommands, albumCommands, currentuserCommands, artistCommands
from functions import spotifymanager


class CLIController:
    def __init__(self):
        self.spotify_manager = spotifymanager.SpotifyManager(
            scope="user-library-read user-read-private user-follow-read playlist-modify-public playlist-modify-private ugc-image-upload user-top-read user-library-modify user-follow-modify"
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
            "-n": {"requires_value": True, "type": int, "multiple_values": False},
            "--num": {"requires_value": True, "type": int, "multiple_values": False},
            "-v": {"requires_value": True, "type": str, "multiple_values": True},
            "--val": {"requires_value": True, "type": str, "multiple_values": True}
        }

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

    def arg_parser(self, args: list, arg_count=1):
        """Parse flags into a clean dictionary of {flag: value(s)}."""
        parsed = {}
        i = 0
        while i < len(args):
            flag = args[i]
            if flag not in self.flags:
                print(f"Unknown argument: {flag}")
                i += 1
                continue

            info = self.flags[flag]

            if info.get("requires_value", False):
                # Multiple values
                if info.get("multiple_values", False) and arg_count > 1:
                    values = []
                    j = i + 1
                    while j < len(args) and args[j] not in self.flags and len(values) < arg_count:
                        try:
                            values.append(info.get("type", str)
                                          (self.strip_URL(args[j])))
                        except ValueError:
                            print(f"Invalid type for flag {flag}: {args[j]}")
                            values.append(None)
                        j += 1

                    if len(values) < arg_count:
                        print(
                            f"Flag {flag} requires {arg_count} values, only {len(values)} given")
                        parsed[flag] = None
                    else:
                        parsed[flag] = values

                    i = j - 1  # skip processed values

                else:  # single value
                    if i + 1 >= len(args) or args[i+1] in self.flags:
                        print(f"Flag {flag} requires a value but none given")
                        parsed[flag] = None
                    else:
                        try:
                            parsed[flag] = info.get("type", str)(args[i + 1])
                        except ValueError:
                            print(f"Invalid type for flag {flag}: {args[i+1]}")
                            parsed[flag] = None
                        i += 1  # skip value
            else:  # flag doesn't require value
                parsed[flag] = True

            i += 1
        return parsed

    def get_flag_values(self, args_dict, flag, prompts):
        values = args_dict.get(flag)
        if not values:
            values = []
            for p in prompts:
                user_input = input(p)
                if not user_input:
                    print("No input provided. Aborting.")
                    return None
                values.append(self.strip_URL(user_input))
        return values

    def cmd_login(self, *args):
        """Login and set the current user"""
        self.currentuser_cmds.cmd_login()
        # Update CLIController's current_user reference
        self.current_user = self.currentuser_cmds.current_user

    def check_string(self, s):
        return (isinstance(s, str) and s.strip() != "")

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
        """Returns Artist's Songs on a Playlist (-v <ARTIST> <PLAYLIST>)"""
        try:
            args_dict = self.arg_parser(args, arg_count=2)
            values = self.get_flag_values(
                args_dict, "-v", ["Enter Artist ID: ", "Enter Playlist ID: "])
            if not values:
                return
            artist_id, playlist_id = values[0], values[1]
            tracks = self.artist_cmds.playlist_tracks(artist_id, playlist_id)
            for t in tracks:
                print(self.song_cmds.get_song_info(t.track_id))

        except Exception as e:
            print(f"Error retrieving artist songs on playlist: {e}")

    # apc - Create Artist Playlist
    '''def cmd_apc(self, *args):
        """Creates a playlist specifically for an artist (-v <ARTIST> <PLAYLIST>)"""
        print("HINT: Enter a random (alphanumeric) value to create a playlist")
        try:
            args_dict = self.arg_parser(args, arg_count=2)
            values = self.get_flag_values(args_dict, "-v", 2, ["Enter Artist ID: ", "HINT: Enter a random (alphanumeric) value to create a playlist\nEnter Playlist ID: "])
            if not values:
                return
            artist_id, playlist_id = values[0], values[1]
            print("Checking for playlist...")
            result = self.playlist_cmds.check_exists(playlist_id)
            if not result:
                playlist_name = input("Create playlist name: ")
                if not playlist_name or playlist_name=="":
                    playlist_name = f"{artist_id} playlist"
                

        Need Playlist Creation implemented
    '''
    # apcp - Create Artist Playlist from Playlist (splice)
    # atg - Artist Genres

    def cmd_atg(self, *args):
        """Returns Artist's Genres (-v <ARTIST>)"""
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
        """Adds song to playlist (-v <TRACK_ID> <PLAYLIST_ID>)"""
        try:
            if not self.current_user:
                print("You must login first")
                return
            args_dict = self.arg_parser(args, arg_count=2)
            values = self.get_flag_values(
                args_dict, "-v", ["Enter Track ID: ", "Enter Playlist ID: "])
            if not values:
                return
            track_id, playlist_id = values[0], values[1]
            self.song_cmds.add_song_to_playlist(
                track_id, playlist_id, current_user=self.current_user)
            print("Added song(s) to playlist")
        except Exception as e:
            print(f"Error adding song to playlist: {e}")

        # spr - Song Playlist Remove
    def cmd_spr(self, *args):
        """Removes song from playlist (-v <TRACK_ID> <PLAYLIST>)"""
        try:
            if not self.current_user:
                print("You must login first")
                return
            args_dict = self.arg_parser(args, arg_count=2)
            values = self.get_flag_values(
                args_dict, "-v", ["Enter Track ID: ", "Enter Playlist ID: "])
            if not values:
                return
            track_id, playlist_id = values[0], values[1]
            self.song_cmds.remove_song_from_playlist(
                track_id, playlist_id, current_user=self.current_user)
            print("Removed song(s) to playlist")
        except Exception as e:
            print(f"Error removing song from playlist: {e}")
        # spl - Song Playlist List

    def cmd_spl(self, *args):
        """Lists whether or not a song is on a playlist (-v <TRACK_ID> -p <PLAYLIST>)"""
        try:
            args_dict = self.arg_parser(args, arg_count=2)
            values = self.get_flag_values(
                args_dict, "-v", ["Enter Track ID: ", "Enter Playlist ID: "])
            if not values:
                return
            track_id, playlist_id = values[0], values[1]
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
    def cmd_p(self, *args):
        """Prints playlist details (-v <PLAYLIST>)"""
        try:
            args_dict = self.arg_parser(args)
            playlist_id = args_dict.get(
                "-v") or self.strip_URL(input("Enter Playlist ID: "))
            print("Getting playlist details...")
            playlist_obj = self.playlist_cmds.get_playlist_info(playlist_id)
            print(f"Playlist Name: {playlist_obj.get_playlist_name()}")
            print(f"Playlist Length: {playlist_obj.get_playlist_length()}")
            print(f"Playlist Image: {playlist_obj.get_playlist_image()}")
            owner = playlist_obj.get_playlist_owner()
            print(f"Playlist Owner: {owner[1]} (id: {owner[0]})")
            print(
                f"Follower Count: {playlist_obj.get_playlist_follower_count()}")
            print(
                f"Playlist Visibility: {'public' if playlist_obj.get_playlist_visibility() == True else 'private'}")
        except Exception as e:
            print(f"Error finding playlist details: {e}")

        # pc - playlist create

    def cmd_pc(self, *args):
        """Creates playlist (-v <NAME>)"""
        try:
            if not self.current_user or not self.currentuser_cmds:
                print("You must login first")
                return
            args_dict = self.arg_parser(args)
            playlist_name = args_dict.get(
                "-v") or input("Enter Playlist Name: ")
            if not playlist_name or playlist_name.strip() == "":
                playlist_name = str(uuid.uuid4())
            options = input(
                "Would you like to provide values for DESCRIPTION, PUBLIC, COLLABORATIVE? [N/y]: ")
            description, public, collaborative = None, True, False  # defaults
            if options == "y":
                description = input(
                    "Enter Playlist Description (or leave blank): ").strip() or None

                public_input = input(
                    "Should the playlist be PUBLIC? [Y/n]: ").strip().lower()
                if public_input == "n":
                    public = False

                collab_input = input(
                    "Should the playlist be COLLABORATIVE? [y/N]: ").strip().lower()
                if collab_input == "y":
                    collaborative = True
            print(f"Creating playlist {playlist_name}...")
            playlist_id = self.currentuser_cmds.create_user_playlist(
                playlist_name, description, public, collaborative, self.current_user)
            print(
                f"Created playlist {playlist_name}! https://spotify.com/playlist/{playlist_id}")
        except Exception as e:
            print(f"Error creating playlist: {e}")

    # pimg - playlist image
    def cmd_pimg(self, *args):
        """Retrieves playlist img URL (-v <PLAYLIST_ID>)"""
        try:
            args_dict = self.arg_parser(args)
            playlist_id = args_dict.get(
                "-v") or input("Enter Playlist Name: ")
            print("Fetching playlist img...")
            playlist = self.playlist_cmds.get_playlist_info(playlist_id)
            img = playlist.get_playlist_image()
            print(
                f"IMG URL for Playlist {playlist.get_playlist_name()}: {img}")

        except Exception as e:
            print(f"Error retrieving playlist img: {e}")

    # pimgr - playlist image replace
    def cmd_pimgr(self, *args):
        """Replaces playlist img by url (-v <PLAYLIST_ID> <IMG_URL>)"""
        try:
            if not self.current_user or not self.currentuser_cmds:
                print("You must login first")
                return
            args_dict = self.arg_parser(args, arg_count=2)
            values = self.get_flag_values(
                args_dict, "-v", ["Enter Playlist ID: ", "Enter Image URL: "])
            if not values:
                return

            playlist_id, image_url = values[0], values[1]

            print(f"Fetching image from {image_url}...")
            response = requests.get(image_url)
            if response.status_code != 200:
                print("Failed to fetch image from URL")
                return
            image_b64 = base64.b64encode(response.content).decode("utf-8")
            print("Uploading playlist image...")
            result = self.playlist_cmds.upload_playlist_image(
                playlist_id=playlist_id, URL=image_b64)
            print(
                f"{'Successfully replaced cover image' if result else 'Failed to replace cover image'}")

        except Exception as e:
            print(f"Error setting playlist img: {e}")

        # ptl - playlist track list

    def cmd_ptl(self, *args):
        """Prints track name(s) and id(s) for playlist (-v <PLAYLIST> -n <NUM_SONGS> (default:20) -a ALL)"""
        try:
            args_dict = self.arg_parser(args)
            playlist_id = args_dict.get(
                "-v") or self.strip_URL(input("Enter Playlist ID: "))
            num_songs = args_dict.get("-n")
            alltracks = args_dict.get("-a")
            if not num_songs and not alltracks:
                print("No song count provided, defaulting to 20")
                num_songs = 20
            if alltracks:
                num_songs = self.playlist_cmds.check_playlist(
                    playlist_id).get_playlist_length()
            track_list = self.playlist_cmds.get_playlist_track_names(
                playlist_id=playlist_id, length=num_songs)
            for i, p in enumerate(track_list.keys()):
                print(f"({i+1}) {track_list[p]}")
        except Exception as e:
            print(f"Error finding playlist tracks: {e}")

        # ptd - playlist track delete at position
    def cmd_ptd(self, *args):
        """Delete a track from a playlist at a certain position (-v <PLAYLIST_ID> <TRACK_ID>)"""
        try:
            if not self.current_user or not self.currentuser_cmds:
                print("You must login first")
                return
            print("WARNING: this function requires a position. If you do not provide, one will be given. Use ptda to get rid of ALL instances")

            args_dict = self.arg_parser(args, arg_count=2)
            values = self.get_flag_values(
            args_dict, "-v", ["Enter Playlist ID: ", "Enter Track ID: "])
            if not values:
                return
            playlist_id, track_id = values[0], values[1]
            position = input("Position of the track in the playlist (number left of track)?: ")
            if not position.isnumeric():
                print("Invalid position. One will be provided")
                position = None
            else:
                position = int(position)
            print("Retrieving playlist tracks")
            tracks = self.playlist_cmds.get_playlist_track_names_and_positions(
            playlist_id=playlist_id)
            track_delete=None
            position_arr=[]
            for t in tracks:
                if t[0] == track_id:
                    track_delete=t[1]
                    position_arr.append(t[1][1]+1)
            if not track_delete:
                print("Track not found on playlist.")
                return
            if not position:
                print("Track found at the following position(s)")
                print("Position(s): " + ", ".join(str(p) for p in position_arr))
                position=input("Please enter the position for track removal: ")
                try:
                    position = int(position)
                except TypeError as e:
                    print("ERROR: Invalid position. Please try again.")
                    return
            if position in position_arr:
                print(f"Removing track at {position}")
                result = self.playlist_cmds.get_playlist_info(playlist_id=playlist_id).remove_specific_track(track_id, position-1, position_arr)
                if result:
                    print("Successfully removed track")
                    return
                print("Failed to return track")
                return
            print("Invalid position. Please try again.")
        except Exception as e:
            print(f"An error occurred while deleting track from playlist: {e}")

    # ptda - playlist track delete all
    def cmd_ptda(self, *args):
        """Delete all instances of a track on a playlist (-v <PLAYLIST_ID> <TRACK_ID>)"""
        try:
            if not self.current_user or not self.currentuser_cmds:
                print("You must login first")
                return
            print("WARNING: this function removes EVERY instance of an object. Use ptd to get rid of SINGLE instances")
            args_dict = self.arg_parser(args, arg_count=2)
            values = self.get_flag_values(
            args_dict, "-v", ["Enter Playlist ID: ", "Enter Track ID: "])
            if not values:
                return
            playlist_id, track_id = values[0], values[1]
            print("Retrieving playlist tracks")
            tracks = self.playlist_cmds.get_playlist_track_names(
            playlist_id=playlist_id)
            track_delete = None
            for t in tracks:
                if t[0] == track_id:
                    track_delete=t
            if not track_delete:
                print("Track not found on playlist")
                return
            print("Removing instances of track")
            result = self.playlist_cmds.get_playlist_info(playlist_id).remove_tracks(track_id)
            if result:
                print("Successfully removed track(s)")
            else:
                print("Failed to remove track(s)")
            return
        except Exception as e:
            print(f"An error occurred while deleting track from playlist: {e}")



    # pd - delete playlist
    def cmd_pd(self,*args):
        """Deletes playlist from user library (-v <PLAYLIST_ID>)"""
        try:
            if not self.current_user or not self.currentuser_cmds:
                print("You must login first")
                return
            args_dict = self.arg_parser(args)
            playlist_id = args_dict.get(
                "-v") or self.strip_URL(input("Enter Playlist ID: "))
            print("Deleting playlist...")
            self.currentuser_cmds.delete_user_playlist(playlist_id)
            print("Deleted playlist!")
            


        except Exception as e:
            print(f"An error occurred while deleting playlist: {e}")



    # ptx - playlist track exchange (replace)

    def cmd_ptx(self, *args):
        """Exchanges (replaces) a song in a playlist with another song (-v <PLAYLIST> <TRACK_ID_TO_REPLACE> <TRACK_ID_TO_ADD>)"""
        try:
            if not self.current_user or not self.currentuser_cmds:
                print("You must login first")
                return
            args_dict = self.arg_parser(args, arg_count=3)
            values = self.get_flag_values(
                args_dict, "-v", ["Enter Playlist ID: ", "Enter Track ID to Replace: ", "Enter Track ID to Add: "])
            if not values:
                return
            playlist_id, track_replace_id, track_add_id = values[0], values[1], values[2]
            print("Retrieving playlist tracks...")
            tracks = self.playlist_cmds.get_playlist_track_names_and_positions(
                playlist_id=playlist_id)
            print("Checking playlist for song...")
            replace_track = None
            for t in tracks:
                if t[0] == track_replace_id:
                    replace_track = t[1]
                    break
            if not replace_track:
                print("Track not found on playlist.")
                return
            print("Found track on playlist, checking existence of other song")
            exist = self.song_cmds.check_exists(track_add_id)
            if not exist:
                print("Track to Add does not exist.")
                return
            # track already made from existence check
            add_track = self.song_cmds.get_song_info(track_add_id)
            print(
                f"Replacing {replace_track[0]} with {add_track.get_track_name()} at position {replace_track[1]}...")
            result = self.playlist_cmds.replace_track_exchange(
                playlist_id, track_replace_id, track_add_id, position=replace_track[1])
            if result:
                print("Track sucessfully replaced!")
            else:
                print("Track exchange failed")
            return
        except Exception as e:
            print(f"An error occurred while exchanging tracks: {e}")

        # ppi - playlist playlist intersection
    def cmd_ppi(self, *args):
        """Intersect playlist tracks (-v <PLAYLIST_1_ID> <PLAYLIST_2_ID> <PLAYLIST_3_ID>)"""
        try:
            if not self.current_user or not self.currentuser_cmds:
                print("You must login first")
                return
            args_dict = self.arg_parser(args, arg_count=3)
            values = self.get_flag_values(
                args_dict, "-v", ["Enter First Playlist ID: ", "Enter Second Playlist ID: ", "Enter Resulting Playlist ID: "])
            if not values:
                return
            first_playlist_id, second_playlist_id, resulting_playlist_id = values[0], values[1], values[2]
            print("Retrieving playlist tracks for first playlist...")
            p1 = self.playlist_cmds.check_exists(first_playlist_id)
            if not p1:
                print("Playlist 1 doesn't exist")
                return
            p1 = self.playlist_cmds.check_playlist(first_playlist_id)
            p1_tracks = p1.get_playlist_track_names(p1.get_playlist_length())
            print("Retrieving playlist tracks for second playlist...")
            p2 = self.playlist_cmds.check_exists(second_playlist_id)
            if not p2:
                print("Playlist 2 doesn't exist")
                return
            p2 = self.playlist_cmds.check_playlist(second_playlist_id)
            p2_tracks = p2.get_playlist_track_names(p2.get_playlist_length())
            print("Checking resulting playlist...")
            p3 = self.playlist_cmds.check_exists(resulting_playlist_id)
            if not p3:
                print("Resulting playlist doesn't exist. Creating now...")
                p3 = self.currentuser_cmds.create_user_playlist(playlist_name=p1.get_playlist_name() + " x " + p2.get_playlist_name(), description="", public=True, collaborative=False)
                print("Playlist created")
            print("Intersecting playlists")
            self.playlist_cmds.intersect_playlists(p1_tracks, p2_tracks, p3)
            print("Intersected playlists!")
        except Exception as e:
            print(f"An error occurred while intersecting playlists: {e}")



        # ppu - playlist playlist union
    def cmd_ppu(self, *args):
        """Union playlist tracks (-v <PLAYLIST_1_ID> <PLAYLIST_2_ID> <PLAYLIST_3_ID>)"""
        try:
            if not self.current_user or not self.currentuser_cmds:
                print("You must login first")
                return
            args_dict = self.arg_parser(args, arg_count=3)
            values = self.get_flag_values(
                args_dict, "-v", ["Enter First Playlist ID: ", "Enter Second Playlist ID: ", "Enter Resulting Playlist ID: "])
            if not values:
                return
            first_playlist_id, second_playlist_id, resulting_playlist_id = values[0], values[1], values[2]
            print("Retrieving playlist tracks for first playlist...")
            p1 = self.playlist_cmds.check_exists(first_playlist_id)
            if not p1:
                print("Playlist 1 doesn't exist")
                return
            p1 = self.playlist_cmds.check_playlist(first_playlist_id)
            p1_tracks = p1.get_playlist_track_names(p1.get_playlist_length())
            print("Retrieving playlist tracks for second playlist...")
            p2 = self.playlist_cmds.check_exists(second_playlist_id)
            if not p2:
                print("Playlist 2 doesn't exist")
                return
            p2 = self.playlist_cmds.check_playlist(second_playlist_id)
            p2_tracks = p2.get_playlist_track_names(p2.get_playlist_length())
            print("Checking resulting playlist...")
            p3 = self.playlist_cmds.check_exists(resulting_playlist_id)
            if not p3:
                print("Resulting playlist doesn't exist. Creating now...")
                p3 = self.currentuser_cmds.create_user_playlist(playlist_name=p1.get_playlist_name() + " x " + p2.get_playlist_name(), description="", public=True, collaborative=False)
                print("Playlist created")
            print("Unioning playlists")
            self.playlist_cmds.union_playlists(p1_tracks, p2_tracks, p3)
            print("Unioned playlists!")
        except Exception as e:
            print(f"An error occurred while unioning playlists: {e}")



        # ppd - playlist playlist difference
    def cmd_ppd(self, *args):
        """Diffentiate playlist tracks (-v <PLAYLIST_1_ID> <PLAYLIST_2_ID> <PLAYLIST_3_ID>)"""
        """P1 but not P2"""
        try:
            if not self.current_user or not self.currentuser_cmds:
                print("You must login first")
                return
            args_dict = self.arg_parser(args, arg_count=3)
            values = self.get_flag_values(
                args_dict, "-v", ["Enter First Playlist ID: ", "Enter Second Playlist ID: ", "Enter Resulting Playlist ID: "])
            if not values:
                return
            first_playlist_id, second_playlist_id, resulting_playlist_id = values[0], values[1], values[2]
            print("Retrieving playlist tracks for first playlist...")
            p1 = self.playlist_cmds.check_exists(first_playlist_id)
            if not p1:
                print("Playlist 1 doesn't exist")
                return
            p1 = self.playlist_cmds.check_playlist(first_playlist_id)
            p1_tracks = p1.get_playlist_track_names(p1.get_playlist_length())
            print("Retrieving playlist tracks for second playlist...")
            p2 = self.playlist_cmds.check_exists(second_playlist_id)
            if not p2:
                print("Playlist 2 doesn't exist")
                return
            p2 = self.playlist_cmds.check_playlist(second_playlist_id)
            p2_tracks = p2.get_playlist_track_names(p2.get_playlist_length())
            print("Checking resulting playlist...")
            p3 = self.playlist_cmds.check_exists(resulting_playlist_id)
            if not p3:
                print("Resulting playlist doesn't exist. Creating now...")
                p3 = self.currentuser_cmds.create_user_playlist(playlist_name=p1.get_playlist_name() + " x " + p2.get_playlist_name(), description="", public=True, collaborative=False)
                print("Playlist created")
            print("Differentiating playlists")
            self.playlist_cmds.differentiate_playlists(p1_tracks, p2_tracks, p3)
            print("Differentiated playlists!")
        except Exception as e:
            print(f"An error occurred while Differentiating playlists: {e}")

    # ptm - playlist track move
    def cmd_ptm(self, *args):
        """Move a track from one position to another in a playlist (-v <PLAYLIST_ID> <TRACK_ID> <NEW_POSITION>)"""
        try:
            if not self.current_user or not self.currentuser_cmds:
                print("You must login first")
                return

            args_dict = self.arg_parser(args, arg_count=3)
            values = self.get_flag_values(
                args_dict, "-v",
                ["Enter Playlist ID: ", "Enter Track ID: ", "Enter New Position: "]
            )
            if not values:
                return

            playlist_id, track_id, new_position = values[0], values[1], values[2]

            if not new_position.isnumeric():
                print("Invalid position. Please enter a number.")
                return
            new_position = int(new_position)

            print("Retrieving playlist tracks...")
            tracks = self.playlist_cmds.get_playlist_track_names_and_positions(
                playlist_id=playlist_id
            )

            # Find current positions of the track
            track_positions = []
            for t in tracks:
                if t[0] == track_id:
                    track_positions.append(t[1][1])  # store 0-based index

            if not track_positions:
                print("Track not found in playlist.")
                return

            print("Track found at the following positions:")
            print("Position(s): " + ", ".join(str(p+1) for p in track_positions))

            # If there are duplicates, ask which one to move
            if len(track_positions) > 1:
                choice = input("Multiple occurrences found. Enter the position of the one you want to move: ")
                if not choice.isnumeric() or int(choice) not in [p+1 for p in track_positions]:
                    print("Invalid choice.")
                    return
                current_position = int(choice) - 1
            else:
                current_position = track_positions[0]

            print(f"Moving track {track_id} from position {current_position+1} to {new_position}...")
            result = self.playlist_cmds.move_track(
                playlist_id, current_position, new_position-1
            )

            if result:
                print("Track successfully moved!")
            else:
                print("Failed to move track.")

        except Exception as e:
            print(f"An error occurred while moving track in playlist: {e}")


       # pdd - playlist details description
    def cmd_pdd(self, *args):
        """Print playlist description details (-v <PLAYLIST_ID>)"""
        try:
            args_dict = self.arg_parser(args)
            playlist_id = args_dict.get(
                "-v") or self.strip_URL(input("Enter Playlist ID: "))
            print("Getting playlist details...")
            playlist_obj = self.playlist_cmds.get_playlist_info(playlist_id)
            print(f"Playlist Description: {playlist_obj.get_playlist_description()}")
        except Exception as e:
            print(f"An error occurred while retrieving playlist description: {e}")

 
        # pdn - playlist details name
    def cmd_pdn(self, *args):
        """Print playlist name (-v <PLAYLIST_ID>)"""
        try:
            args_dict = self.arg_parser(args)
            playlist_id = args_dict.get(
                "-v") or self.strip_URL(input("Enter Playlist ID: "))
            print("Getting playlist details...")
            playlist_obj = self.playlist_cmds.get_playlist_info(playlist_id)
            print(f"Playlist Name: {playlist_obj.get_playlist_name()}")
        except Exception as e:
            print(f"An error occurred while retrieving playlist name: {e}")

        # pdp - playlist details public
    def cmd_pdp(self, *args):
        """Print playlist visibility (-v <PLAYLIST_ID>)"""
        try:
            args_dict = self.arg_parser(args)
            playlist_id = args_dict.get(
                "-v") or self.strip_URL(input("Enter Playlist ID: "))
            print("Getting playlist details...")
            playlist_obj = self.playlist_cmds.get_playlist_info(playlist_id)
            print(f"Playlist Visibility: {'Public' if playlist_obj.get_playlist() == True else 'Private'}")
        except Exception as e:
            print(f"An error occurred while retrieving playlist name: {e}")
    
        # pta - playlist track add
        # pti - playlist track(s) insert (in) spot (-s)

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

    # Current User
    # cus - Return Current User Settings

    def cmd_cus(self, *args):
        """Retrieves user setting(s) for Current User (-v SETTING, -a ALL (default))"""

        try:
            if not self.current_user or not self.currentuser_cmds:
                print("You must login first")
                return
            args_dict = self.arg_parser(args)
            setting = args_dict.get(
                "-v") or None
            if setting:
                print(
                    f"Retrieving {setting} User Setting for {self.current_user.user_id}")
                result = self.currentuser_cmds.current_user.get_specific_user_settings(
                    setting=setting)
            else:
                print(
                    f"Retrieving User Settings for {self.currentuser_cmds.current_user.user_id}")
                result = self.currentuser_cmds.current_user.get_user_settings()
            print(result)
        except Exception as e:
            print(f"Error retrieving user settings: {e}")

    # cuss - Set user setting
    def cmd_cuss(self, *args):
        """Sets user setting for Current User (-v SETTING VALUE)"""
        try:
            if not self.current_user or not self.currentuser_cmds:
                print("You must login first")
                return
            args_dict = self.arg_parser(args)
            values = self.get_flag_values(
                args_dict, "-v", ["Enter Setting: ", "Enter Value: "])
            if not values:
                return
            setting = values[0]
            value = values[1]
            print(
                f"Setting User Setting {setting} to {value} for {self.currentuser_cmds.current_user.user_id}")
            self.currentuser_cmds.current_user.set_specific_user_settings(
                setting, value)
            print(
                f"Set {setting} to {value} for {self.currentuser_cmds.current_user.user_id}")
        except Exception as e:
            print(f"Error setting user settings: {e}")
