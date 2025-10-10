import json
import os


class SettingsManager:
    def __init__(self, user_id, current_user, base_path="./functions/database/temp_settings"):  # Change to API
        self.user_id = user_id
        self.current_user = current_user
        self.base_path = base_path
        os.makedirs(self.base_path, exist_ok=True)
        self.settings_file = os.path.join(
            self.base_path, f"{self.user_id}_settings.json")
        self.settings = self._load()
        if not os.path.exists(self.settings_file):
            print("Settings file not found. Creating one now...")
            self.save()
    def _load(self):
        if os.path.exists(self.settings_file):
            with open(self.settings_file, "r") as f:
                return json.load(f)
        return {"user_id": self.user_id,
                "properties": {
                    "artist_playlist_json": {}
                }}

    def save(self):
        with open(self.settings_file, "w") as f:
            json.dump(self.settings, f, indent=4)

    def set(self, key, value):
        keys = key.split("/")
        d = self.settings
        for k in keys[:-1]:
            if k not in d or not isinstance(d[k], dict):
                d[k] = {}
            d = d[k]
        d[keys[-1]] = value
        self.save()

    def get(self, key, default=None):
        keys = key.split("/")
        d = self.settings
        for k in keys:
            if isinstance(d, dict) and k in d:
                d = d[k]
            else:
                return default #Path Doesnt Exist
        return d
