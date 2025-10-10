import { BaseAPI } from "./API_index";

/**
 * Get current user profile
 * @param {boolean} raw - whether to fetch raw data
 */
export const getUserProfile = ({ raw = false } = {}) => {
  const params = new URLSearchParams();
  if (raw) params.append("raw", "true");
  return BaseAPI.get(`/me/get?${params.toString()}`);
};

/**
 * Get user's top tracks
 * @param {number} count - number of tracks
 * @param {string} time_range - 'short_term', 'medium_term', or 'long_term'
 */
export const getUserTopTracks = ({ count = 10, time_range = "medium_term" } = {}) => {
  const params = new URLSearchParams({ count, time_range });
  return BaseAPI.get(`/me/top/tracks?${params.toString()}`);
};


/**
 * Get user's top artists
 * @param {number} count
 * @param {string} time_range
 */
export const getUserTopArtists = ({ count = 10, time_range = "medium_term" } = {}) => {
  const params = new URLSearchParams({ count, time_range });
  return BaseAPI.get(`/me/top/artists?${params.toString()}`);
};

/**
 * Get user's full library
 */
export const getUserLibrary = () => BaseAPI.get("/me/library");

/**
 * Follow a user
 */
export const followUser = (userId) => BaseAPI.put(`/me/follow/user/${userId}`);

/**
 * Unfollow a user
 */
export const unfollowUser = (userId) => BaseAPI.delete(`/me/unfollow/user/${userId}`);

/**
 * Follow an artist
 */
export const followArtist = (artistId) => BaseAPI.put(`/me/follow/artist/${artistId}`);

/**
 * Unfollow an artist
 */
export const unfollowArtist = (artistId) => BaseAPI.delete(`/me/unfollow/artist/${artistId}`);

/**
 * Follow a playlist
 */
export const followPlaylist = (playlistId) => BaseAPI.put(`/me/follow/playlist/${playlistId}`);

/**
 * Unfollow a playlist
 */
export const unfollowPlaylist = (playlistId) => BaseAPI.delete(`/me/unfollow/playlist/${playlistId}`);



/**
 * Save tracks
 * @param {string|string[]} trackIds
 */
export const saveTracks = (trackIds) => {
  if (!Array.isArray(trackIds)) trackIds = [trackIds];
  return BaseAPI.put(`/me/save/track/${trackIds.join(",")}`);
};

/**
 * Delete saved tracks
 * @param {string|string[]} trackIds
 */
export const deleteSavedTracks = (trackIds) => {
  if (!Array.isArray(trackIds)) trackIds = [trackIds];
  return BaseAPI.delete(`/me/delete/track/${trackIds.join(",")}`);
};

/**
 * Save albums
 * @param {string|string[]} albumIds
 */
export const saveAlbums = (albumIds) => {
  if (!Array.isArray(albumIds)) albumIds = [albumIds];
  return BaseAPI.put(`/me/save/album/${albumIds.join(",")}`);
};

/**
 * Delete saved albums
 * @param {string|string[]} albumIds
 */
export const deleteSavedAlbums = (albumIds) => {
  if (!Array.isArray(albumIds)) albumIds = [albumIds];
  return BaseAPI.delete(`/me/delete/album/${albumIds.join(",")}`);
};

/** ---------------------------
 * Playlists
 * --------------------------- */

/**
 * Create a playlist
 */
export const createPlaylist = ({ name = "New Playlist", description = "", _public = true, collaborative = false } = {}) => {
  const params = new URLSearchParams({ name, description, _public, collaborative });
  return BaseAPI.post(`/me/create/playlist?${params.toString()}`);
};

/**
 * Delete a playlist
 */
export const deletePlaylist = (playlistId) => BaseAPI.delete(`/me/delete/playlist/${playlistId}`);
/**
 * Get user playlists
 */
export const getUserPlaylists = () => BaseAPI.get("/me/playlists");

/**
 * Get user playlists
 */
export const getUserArtists = () => BaseAPI.get("/me/artists");

/**
 * Get user albums
 */
export const getUserAlbums = () => BaseAPI.get("/me/albums");

/**
 * Get user tracks
 */
export const getUserTracks = () => BaseAPI.get("/me/tracks");


/** ---------------------------
 * Devices
 * --------------------------- */

/**
 * Get user devices
 */
export const getUserDevices = () => BaseAPI.get("/me/devices");