import { BaseAPI } from "./API_index";

/**
 * Search Spotify
 * @param {string} query - Search query string
 * @param {object} options - Search options
 * @param {string} options.type - One of "album", "artist", "playlist", "track", "show", "episode", "audiobook"
 * @param {number} options.limit - Number of results to return (default 20)
 * @param {number} options.offset - Offset for pagination (default 0)
 */
export const searchSpotify = async (query, { type, limit = 20, offset = 0 } = {}) => {
  if (!query) throw new Error("Query is required");
  if (!type) throw new Error("Search type is required");

  const params = new URLSearchParams({
    search_type: type,
    limit: limit.toString(),
    offset: offset.toString(),
  });

  return BaseAPI.get(`/search/${encodeURIComponent(query)}?${params.toString()}`);
};
