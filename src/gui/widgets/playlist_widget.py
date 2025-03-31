import tkinter as tk
from PIL import Image, ImageTk
import requests
from io import BytesIO
from src.api.functions.playlist import Playlist

class PlaylistWidget(tk.Frame):
    def __init__(self, master=None, playlist=None, width=400, height=200):
        super().__init__(master)
        self.master = master
        self.playlist = playlist

        self.img_url = self.playlist.get_playlist_image()
        self.length = self.playlist.get_playlist_length()
        self.name = self.playlist.get_playlist_name()

        self.width = width
        self.height = height

        self.configure(width=width, height=height)
        self.grid()

        self.txt = tk.Label(self, text=self.name)
        self.txt.grid(row=0, column=2, padx=10, pady=10)

        self.len = tk.Label(self, text=f"{self.length} tracks")
        self.len.grid(row=1, column=2, padx=10, pady=10)

        if self.img_url:
            try:
                response = requests.get(self.img_url)
                image_data = BytesIO(response.content)
                pil_img = Image.open(image_data)
                pil_img = pil_img.resize((100, 100))  
                tk_img = ImageTk.PhotoImage(pil_img)

                self.img_label = tk.Label(self, image=tk_img)
                self.img_label.image = tk_img  
                self.img_label.grid(row=0, column=1, rowspan=2, padx=10, pady=10)

            except Exception as e:
                print(f"Failed to load image: {e}")

