import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

import tkinter as tk
from src.gui.widgets.playlist_widget import PlaylistWidget
from src.api.functions.spotifymanager import SpotifyManager


SM = SpotifyManager(scope="playlist-modify-public", username="9yiidfk1ydpewq4u1ge28fidh")


window = tk.Tk()
window.title("SpotifyHub")
window.geometry("800x600")


canvas = tk.Canvas(window)
scrollbar = tk.Scrollbar(window, orient="vertical", command=canvas.yview)
scrollable_frame = tk.Frame(canvas)


scrollable_frame.bind(
    "<Configure>",
    lambda e: canvas.configure(
        scrollregion=canvas.bbox("all")
    )
)

canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
canvas.configure(yscrollcommand=scrollbar.set)


canvas.pack(side="left", fill="both", expand=True)
scrollbar.pack(side="right", fill="y")


user = SM.get_user()
for playlist in user.get_user_playlists():
    PlaylistWidget(master=scrollable_frame, playlist=playlist)


window.mainloop()
