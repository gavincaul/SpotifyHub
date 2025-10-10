import { BaseAPI } from "./API_index";

/**
 * Get album details
 * @param {string} albumId
 * @param {boolean} raw - whether to fetch raw album data
 */
export const getAlbum = (albumId, { raw = false } = {}) => {
  const params = new URLSearchParams();
  if (raw) params.append("raw", "true");
  return BaseAPI.get(`/album/get/${albumId}?${params.toString()}`);
};

/**
 * Get album tracks
 * @param {string} albumId
 * @param {boolean} positions - whether to include track positions
 */
export const getAlbumTracks = (albumId, { positions = false } = {}) => {
  const params = new URLSearchParams();
  if (positions) params.append("positions", "true");
  return BaseAPI.get(`/album/get_tracks/${albumId}?${params.toString()}`);
};

/**
 * Check if album exists
 * @param {string} albumId
 */
export const checkAlbumExists = (albumId) => {
  return BaseAPI.get(`/album/check_exists/${albumId}`);
};

/**
 * Get album artists
 * @param {string} albumId
 */
export const getAlbumArtists = (albumId) => {
  return BaseAPI.get(`/album/artists/${albumId}`);
};
