import { BaseAPI } from "./API_index";

/**
 * Get detailed info about a song
 * @param {string} songId - Spotify track ID
 * @param {object} options - Optional settings
 * @param {boolean} options.raw - Return raw Spotify data
 */
export const getSong = (songId, { raw = false } = {}) => {
  const params = new URLSearchParams();
  if (raw) params.append("raw", "true");

  return BaseAPI.get(`/song/get/${songId}?${params.toString()}`);
};

/**
 * Check if a song exists in the Spotify catalog
 * @param {string} songId - Spotify track ID
 */
export const checkSongExists = (songId) => {
  return BaseAPI.get(`/song/check_exists/${songId}`);
};

/**
 * Check if a song exists in a specific playlist
 * @param {string} songId - Spotify track ID
 * @param {string} playlistId - Spotify playlist ID
 */
export const checkSongOnPlaylist = (songId, playlistId) => {
  return BaseAPI.get(`/song/check_playlist/${songId}/${playlistId}`);
};
