from functions.models import playlist, user, song, album, currentuser
from functions import spotifymanager

class CLIController:
    def __init__(self):
        self.spotify_manager = spotifymanager.SpotifyManager(scope="user-library-read user-read-private user-follow-read playlist-modify-public user-top-read")
        self.current_user = None

    def cmd_login(self):
        if self.spotify_manager.login_oauth():
            user_id = self.spotify_manager.get_current_user_id()
            if user_id:
                self.current_user = currentuser.CurrentUser(self.spotify_manager)
                print(f"Logged in as {user_id}")
            else:
                print("Failed to get user info after login.")
        else:
            print("Login failed or cancelled.")

    def arg_parser(self, args):
        argument_dictionary = {
            "-a": 0, "--all": 0,
            "-n": 1, "--num": 1,
            "-v": 1, "--val": 1,
        }
        argument_value_dictionary = {
            "-a": 1, "--all": 1,
            "-n": 2, "--num": 2,
            "-v": 3, "--val": 3,
        }
        
        if len(args)==0:
            return {"code":0,"value":None} #default
        
        flag = args[0]
        if flag not in argument_dictionary:
            print(f"Unknown argument: {flag}")
            return {"code": 0, "value": None}
        arg_requirement = argument_dictionary[flag]

        if arg_requirement == 0:
            if len(args) > 1:
                print(f"Flag {flag} takes no additional arguments. Ignoring additional arguments")
            return {"code": argument_value_dictionary[flag], "value": None}
        else:
            if len(args) < 2:
                print(f"Flag {flag} requires {arg_requirement} values. Ignoring command")
                return {"code": -1, "value": None}
            value = args[1]
            match argument_value_dictionary[flag]:
                case 2: # n
                    try:
                        value = int(value)
                        return {"code": 2, "value": value}
                    except ValueError:
                        print(f"Flag {flag} requires an integer. Ignoring command")
                        return {"code": -1, "value": None}
                case 3:
                    if not (isinstance(value, str) and value.strip() != ""):
                        print(f"Flag {flag} requires a string. Ignoring flag")
                        return {"code": -1, "value": value}
                    else:
                        return {"code": 3, "value": value}

    def check_string(s):
        return (isinstance(s, str) and s.strip() != "")           
                    



    def print_playlists(self, playlists):
        if len(playlists) == 0:
            print("No playlists found")
            return
        for i, pl in enumerate(playlists):
            print(f"{i} - {pl.get_playlist_name()} ({pl.get_playlist_length()} tracks)")


    def prompt_time_range(self):
        time_range_map = {"s": "short_term", "m": "medium_term", "l": "long_term"}
        descriptions = {"s": "short term: 4 weeks", "m": "medium term: 6 months", "l": "long term: ~1 year"}

        while True:
            print("Time range options:")
            for key, desc in descriptions.items():
                print(f"  {key}: {desc}")
            selection = input("Please select a time range (s/m/l) or 'q' to cancel: ").strip().lower()

            if selection == "q":
                print("Cancelling command with no execution")
                return None
            if selection in time_range_map:
                return time_range_map[selection]

            print("Invalid input. Please try again.")
    

    # Album
    # b - Get Album
    # bl - Album (track) list
    # ba - Album Artist
    # bs - Album Save
    # bu - Album Unsave




    # Artist
    # a - Artist details
    # at - Artist Top Tracks (-a -n)
    # aa - Artist Top Albums
    # ar - Artist Related
    # ap - Artist Song's on Playlist
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

    def cmd_p(self, *args):
        """Returns Playlist Information (-v <PLAYLIST>)"""
        check_arg = self.arg_parser(args)
        match check_arg["code"]:
            case -1: 
                pass
            case 0: # default
                pid = input("Enter Playlist ID:")
                try:
                    result = self.sp.playlist(pid)
                    print(result)
                except:
                    print("Unable to retrieve playlist information")
            case 3: # -v User Profile Value
                try:
                    result = self.spotify_manager.sp.playlist(check_arg["value"]) != -1
                    print(result)
                except:
                    print("Unable to retrieve playlist information")
            case _:
                print("Invalid argument for function: p")
                print("Ignoring command")


    '''def cmd_pt(self, *args):
        """Returns Playlist Tracks (-v <PLAYLIST>)"""
        check_arg = self.arg_parser(args)
        match check_arg["code"]:
            case -1: 
                pass
            case 0: # default
                pid = input("Enter Playlist ID:")
                try:
                    result = self.sp.playlist(pid)
                    p = playlist.Playlist(self.spotify_manager, pid)
                except:
                    print("Unable to retrieve playlist information")
            case 3: # -v User Profile Value
                try:
                    result = self.spotify_manager.sp.playlist(check_arg["value"]) != -1
                    print(result)
                except:
                    print("Unable to retrieve playlist information")
            case _:
                print("Invalid argument for function: p")
                print("Ignoring command")
                
                need -a -n ^
                '''
    
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

    # usb - User Saved Albums

    def cmd_u(self, *args):
        """Returns User information (-v <USER>)"""
        check_arg = self.arg_parser(args)
        match check_arg["code"]:
            case -1: 
                pass
            case 0: # default
                if not self.current_user:
                    print("No user currently signed in. Use 'login' to sign in, or check a specific User by first using ulf -v <USER>")
                    return
                print("Current User Data:")
                print(self.current_user.get_user_profile())
                return
            case 3: # -v User Profile Value
                result = self.spotify_manager.get_user_profile(check_arg["value"]) != -1
                if result != -1: #Failed to retrieve info
                    print(result)
                    
            case _:
                print("Invalid argument for function: u")
                print("Ignoring command")


    def cmd_ulf(self, *args): #User List FollowerS
        """Returns User's Follower Count (-v <USER>)"""
        check_arg = self.arg_parser(args)
        match check_arg["code"]:
            case -1:
                pass
            case 0:
                if not self.current_user:
                    print("You must login first with 'login', or check a specific User by first using ulf -v <USER>")
                    return
                result = self.spotify_manager.get_user_profile(self.current_user.user_id)
                if result != -1:
                    print(f"User found")
                print(f"User {result['display_name']}: {result['followers']['total']}")
            case 3:
                result = self.spotify_manager.get_user_profile(check_arg["value"])
                if result != -1:
                    print(f"User found")
                print(f"User {result['display_name']}: {result['followers']['total']}")
            case _:
                print("Invalid argument for function: ulf")
                print("Ignoring command")



    def cmd_ulfg(self, *args): #User List FollowinG
        """Returns User's Following List ()"""
        check_arg = self.arg_parser(args)
        match check_arg["code"]:
            case -1:
                pass
            case 0:
                if not self.current_user:
                    print("You must login first with 'login'")
                    return
                following = self.current_user.get_user_following()
                print(following)
            
            case _:
                print("Invalid argument for function: ulfg")
                print("Ignoring command")

    def cmd_ulp(self, *args):
        """Lists a User's Playlists (-a, -n <num>, -v <user>)"""
        check_arg = self.arg_parser(args)
        match check_arg["code"]:
            case -1: 
                pass
            case 0: # default
                if not self.current_user:
                    print("You must login first with 'login' or check a specific User by first using ulp -v <USER>")
                    return
                playlists = self.current_user.get_user_playlists(total=10)
                self.print_playlists(playlists)
            case 1:
                if not self.current_user:
                    print("You must login first with 'login' or check a specific User by first using ulp -v <USER>")
                    return
                playlists = self.current_user.get_user_playlists(total=None)
                self.print_playlists(playlists)
            case 2:
                if not self.current_user:
                    print("You must login first with 'login' or check a specific User by first using ulp -v <USER>")
                    return
                playlists = self.current_user.get_user_playlists(total=check_arg["value"])
                self.print_playlists(playlists)
            case 3:
                result = self.spotify_manager.get_user_profile(check_arg["value"])
                if result != -1:
                    print(f"User found")
                    value = input("Enter number of playlists to retrieve (default 10) (enter 'a' for all): ")
                    if value.strip() == "a":
                        u = user.User(spotify_manager=self.spotify_manager, user_id=result["id"])
                        playlists = u.get_user_playlists(total=None)
                        self.print_playlists(playlists)
                    else: 
                        try:
                            if value.strip() == "":
                                value = 10
                            value = int(value)
                            u = user.User(spotify_manager=self.spotify_manager, user_id=result["id"])
                            playlists = u.get_user_playlists(value)
                            self.print_playlists(playlists)
                        except Exception as e:
                            print(f"Flag requires an integer. Ignoring command\n")


                else:
                    print("User not found. Ignoring Command")
            case _:
                print("Invalid argument for function: ulp")
                print("Ignoring command")

    def cmd_ultt(self, *args):
            """User List Top Tracks (-n, -a)"""
            check_arg = self.arg_parser(args)
            selection = self.prompt_time_range()
            if not selection:
                return
            match check_arg["code"]:
                case -1: 
                    pass
                case 0: # default
                    if not self.current_user:
                        print("You must login first with 'login'")
                        return
                    tracks = self.current_user.get_user_top_tracks(total = 10, time_range=selection)
                    for t in tracks:
                        print(t)
                case 1:
                    if not self.current_user:
                        print("You must login first with 'login'")
                        return
                    tracks = self.current_user.get_user_top_tracks(time_range=selection)
                    for t in tracks:
                        print(t)
                case 2:
                    if not self.current_user:
                        print("You must login first with 'login'")
                        return
                    tracks = self.current_user.get_user_top_tracks(total = check_arg["value"], time_range=selection)
                    for t in tracks:
                        print(t)
                case _:
                    print("Invalid argument for function: ultt")
                    print("Ignoring command")




    def cmd_ulta(self, *args):
            """User List Top Artists (-n, -a)"""
            check_arg = self.arg_parser(args)
            selection = self.prompt_time_range()
            if not selection:
                return
            match check_arg["code"]:
                case -1: 
                    pass
                case 0: # default
                    if not self.current_user:
                        print("You must login first with 'login'")
                        return
                    tracks = self.current_user.get_user_top_artists(total = 10, time_range=selection)
                    for t in tracks:
                        print(t)
                case 1:
                    if not self.current_user:
                        print("You must login first with 'login'")
                        return
                    tracks = self.current_user.get_user_top_tracks()
                    for t in tracks:
                        print(t)
                case 2:
                    if not self.current_user:
                        print("You must login first with 'login'")
                        return
                    tracks = self.current_user.get_user_top_artists(total = check_arg["value"], time_range=selection)
                    for t in tracks:
                        print(t)
                case _:
                    print("Invalid argument for function: ultt")
                    print("Ignoring command")


    def cmd_ufp(self, *args):
        """User follow playlist (-v)"""
        check_arg = self.arg_parser(args)
        match check_arg["code"]:
            case -1:
                pass
            case 0:
                if not self.current_user:
                    print("You must login first with 'login'")
                    return
                playlist_id = input("Provide playlist id: ")
                try:
                    playlist_data = self.sp.playlist(playlist_id)
                except Exception as e:
                    print(f"Playlist not found or inaccessible: {e}")
                    return
                self.sp.current_user.follow_playlist(playlist_id)
            case 2:
                if not self.current_user:
                    print("You must login first with 'login'")
                    return
                self.sp.current_user.follow_playlist(playlist_id)
            case _:
                print("Invalid argument for function: ufp")
                print("Ignoring command")
    def cmd_ufpu(self, *args):
        """User UNfollow playlist (-v)"""
        check_arg = self.arg_parser(args)
        match check_arg["code"]:
            case -1:
                pass
            case 0:
                if not self.current_user:
                    print("You must login first with 'login'")
                    return
                playlist_id = input("Provide playlist id: ")
                try:
                    playlist_data = self.sp.playlist(playlist_id)
                except Exception as e:
                    print(f"Playlist not found or inaccessible: {e}")
                    return
                self.sp.current_user.unfollow_playlist(playlist_id)
            case 2:
                if not self.current_user:
                    print("You must login first with 'login'")
                    return
                self.sp.current_user.unfollow_playlist(playlist_id)
            case _:
                print("Invalid argument for function: ufp")
                print("Ignoring command")

    

    

        


                
                