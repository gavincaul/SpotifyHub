import { BaseAPI } from "./API_index";

/**
 * Get artist details
 * @param {string} artistId
 * @param {boolean} raw - whether to fetch raw artist data
 */
export const getArtist = (artistId, { raw = false } = {}) => {
  const params = new URLSearchParams();
  if (raw) params.append("raw", "true");
  return BaseAPI.get(`/artist/get/${artistId}?${params.toString()}`);
};

/**
 * Check if an artist exists
 * @param {string} artistId
 */
export const checkArtistExists = (artistId) => {
  return BaseAPI.get(`/artist/check_exists/${artistId}`);
};

/**
 * Get top tracks of an artist
 * @param {string} artistId
 * @param {boolean} raw - whether to fetch raw track data
 */
export const getArtistTopTracks = (artistId, { raw = false } = {}) => {
  const params = new URLSearchParams();
  if (raw) params.append("raw", "true");
  return BaseAPI.get(`/artist/top_tracks/${artistId}?${params.toString()}`);
};

/**
 * Get top albums of an artist
 * @param {string} artistId
 * @param {Object} options - optional filters for album types
 * @param {boolean} options.includeSingles
 * @param {boolean} options.includeAppearsOn
 * @param {boolean} options.includeCompilation
 */
export const getArtistTopAlbums = (
  artistId,
  { includeSingles = false, includeAppearsOn = false, includeCompilation = false } = {}
) => {
  const params = new URLSearchParams();
  if (includeSingles) params.append("include_singles", "true");
  if (includeAppearsOn) params.append("include_appears_on", "true");
  if (includeCompilation) params.append("include_compilation", "true");
  return BaseAPI.get(`/artist/top_albums/${artistId}?${params.toString()}`);
};

/**
 * Get genres of an artist
 * @param {string} artistId
 */
export const getArtistGenres = (artistId) => {
  return BaseAPI.get(`/artist/genres/${artistId}`);
};
