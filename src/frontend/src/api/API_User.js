import { BaseAPI } from "./API_index";

/**
 * Get detailed info about a user
 * @param {string} userId - Spotify user ID
 * @param {object} options - Optional settings
 * @param {boolean} options.raw - Return raw Spotify data
 */
export const getUser = (userId, { raw = false } = {}) => {
  const params = new URLSearchParams();
  if (raw) params.append("raw", "true");

  return BaseAPI.get(`/user/get/${userId}?${params.toString()}`);
};

/**
 * Check if a user exists in Spotify
 * @param {string} userId - Spotify user ID
 */
export const checkUserExists = (userId) => {
  return BaseAPI.get(`/user/check_exists/${userId}`);
};

/**
 * Get a user's playlists
 * @param {string} userId - Spotify user ID
 */
export const getUserPlaylists = (userId) => {
  return BaseAPI.get(`/user/playlists/${userId}`);
};
