export const stripURL = (s) => {
    if (!s || typeof s !== 'string' || s.trim() === "") return s;
    if (s.includes("spotify.com")) {
      const parts = s.split("/");
      if (parts.length > 0) {
        let lastPart = parts[parts.length - 1];
        if (lastPart.includes("?")) {
          lastPart = lastPart.split("?")[0];
        }
        return lastPart;
      }
    }
    return s.trim();
  };

export const missing_file_url = "https://static.thenounproject.com/png/3647578-200.png"