import { BaseAPI } from "./API_index";

export const getPlaylist = (playlistId, { raw = false } = {}) => {
  const params = new URLSearchParams();
  if (raw) params.append("raw", "true");

  return BaseAPI.get(`/playlist/get/${playlistId}?${params.toString()}`);
};

export const getPlaylistTracks = (playlistId: string, { total, raw = false }: { total?: number; raw?: boolean } = {}) => {
  const params = new URLSearchParams();
  if (raw) params.append("raw", "true");
  if (typeof total === "number") params.append("total", total.toString()); // <-- send total
  return BaseAPI.get(`/playlist/tracks/${playlistId}?${params.toString()}`);
};
export const getPlaylistImage = (playlistId) => {
  return BaseAPI.get(`/playlist/image/${playlistId}`);
};

export const uploadPlaylistCover = async (playlistId, image) => {
  let body;
  let headers = {};

  if (image instanceof File) {
    // File upload
    body = new FormData();
    body.append("image", image);
    headers["Content-Type"] = "multipart/form-data";
  } else if (typeof image === "string" && image.trim() !== "") {
    // URL upload
    body = { url: image.trim() };
    headers["Content-Type"] = "application/json";
  } else {
    throw new Error("Invalid image: must be a File or a non-empty URL string");
  }

  return BaseAPI.put(`/playlist/upload/cover/${playlistId}`, body, { headers });
};


export const intersectPlaylists = async (p1, p2, p3) => {
  if (!p1 || !p2 || !p3) {
    throw new Error("All three playlist IDs are required");
  }

  const body = { p1, p2, p3 };

  return BaseAPI.post("/playlist/intersect", body, {
    headers: { "Content-Type": "application/json" },
  });
};

export const unionPlaylists = async (p1, p2, p3) => {
  if (!p1 || !p2 || !p3) {
    throw new Error("All three playlist IDs are required");
  }

  const body = { p1, p2, p3 };

  return BaseAPI.post("/playlist/union", body, {
    headers: { "Content-Type": "application/json" },
  });
};

export const differentiatePlaylists = async (p1, p2, p3) => {
  if (!p1 || !p2 || !p3) {
    throw new Error("All three playlist IDs are required");
  }

  const body = { p1, p2, p3 };

  return BaseAPI.post("/playlist/differentiate", body, {
    headers: { "Content-Type": "application/json" },
  });
};

/**
 * Move tracks within a playlist
 * @param {string} playlistId - The playlist ID
 * @param {number[]} fromPositions - Array of track indices to move
 * @param {number} toPosition - Destination index to start moving tracks
 */
export const moveTracks = async (playlistId, fromPositions, toPosition) => {
  if (!playlistId || !fromPositions || toPosition === undefined) {
    throw new Error("playlistId, fromPositions, and toPosition are required");
  }

  const body = { fromPositions, toPosition };

  return BaseAPI.put(`/playlist/move_tracks/${playlistId}`, body, {
    headers: { "Content-Type": "application/json" },
  });
};


/**
 * Add a track to a playlist
 * @param {string} playlistId - The playlist ID
 * @param {string} trackId - The Spotify track ID to add
 * @param {number} [position] - Optional position to insert the track
 */
export const addTrackToPlaylist = async (playlistId, trackId, position) => {
  if (!playlistId || !trackId) {
    throw new Error("playlistId and trackId are required");
  }

  const params = new URLSearchParams();
  params.append("track_id", trackId);
  if (position !== undefined) params.append("position", position);

  return BaseAPI.put(`/playlist/add/${playlistId}?${params.toString()}`);
};


export const getArtistsTracksOnPlaylist = async (playlistId, artists) => {
  if (!playlistId || !artists) {
    throw new Error("playlistId and artist IDs are required");
  }

  const params = new URLSearchParams();
  artists.forEach((artist) => params.append("artists", artist));

  return BaseAPI.get(`/playlist/get/artists_tracks/${playlistId}?${params.toString()}`);
};