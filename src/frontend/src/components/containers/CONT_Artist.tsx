import React, { useEffect, useState } from "react";
import "./CONT_Artist.css";
import Loading from "../ui/elements/Loading.tsx";
import TrackModel from "./items/ITEM_Track.tsx";
import AlbumModel from "./items/ITEM_Album.tsx";
import {
  getArtistTopTracks,
  getArtistTopAlbums,
} from "../../api/API_Artist.js";
import {
  ArtistType,
  TrackType,
  AlbumType,
} from "../../utils/types/ModelTypes.ts";
import RefreshIcon from "../ui/icons/RefreshIcon.tsx";
import { useTheme } from "../../utils/theme/ThemeContext.tsx";

export default function ArtistContainer({ artist }: { artist: ArtistType }) {
  const [topTracks, setTopTracks] = useState<TrackType[]>([]);
  const [albums, setAlbums] = useState<AlbumType[]>([]);
  const [filters, setFilters] = useState({
    album: true,
    single: true,
    compilation: true,
    appears_on: true,
  });
  const [albumsLoading, setAlbumsLoading] = useState(true);
  const [tracksLoading, setTracksLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const { theme } = useTheme();

  useEffect(() => {
    fetchArtistTracks();
    fetchArtistAlbums();
  }, [artist]);

  const fetchArtistTracks = async () => {
    try {
      setTracksLoading(true);
      setError(null);
      const tracksRes = await getArtistTopTracks(artist.id);
      setTopTracks(tracksRes?.tracks || []);
    } catch (err: any) {
      console.error("Error fetching artist:", err);
      setError(err.message || "Failed to load artist data");
    } finally {
      console.log("setTracks");
      setTracksLoading(false);
    }
  };

  const fetchArtistAlbums = async () => {
    try {
      setAlbumsLoading(true);
      setError(null);
      const topAlbums = await getArtistTopAlbums(artist.id, {
        includeAppearsOn: true,
        includeCompilation: true,
        includeSingles: true,
      });
      setAlbums(topAlbums?.albums || []);
    } catch (err: any) {
      console.error("Error fetching artist albums:", err);
      setError(err.message || "Failed to load artist albums");
    } finally {
      setAlbumsLoading(false);
    }
  };
  const handleFilterChange = (filterType: keyof typeof filters) => {
    setFilters((prev) => ({
      ...prev,
      [filterType]: !prev[filterType],
    }));
  };

  const filteredAlbums = albums.filter(
    (album) => filters[album.type as keyof typeof filters]
  );
  if (error) return <div className="artist-error">Error: {error}</div>;

  return (
    <div className="artist-model">
      {/* Top row: cover left, metadata right */}
      <div className="artist-top">
        <div className="artist-cover-wrap">
          <img
            src={artist.images.large}
            alt={`${artist.name} cover`}
            className="artist-cover"
          />
        </div>

        <div className="artist-meta">
          <div className="artist-meta-inner">
            <h2 className="artist-title">{artist.name}</h2>
            <div className="artist-desc">{artist.popularity}</div>
          </div>
        </div>
      </div>

      {/* Two columns layout */}
      <div className="artist-columns-container">
        {/* Left Column - Tracks */}
        <div className="artist-column artist-column-left">
          <div className="artist-toolbar">
            <div className="artist-toolbar-left">
              <span>Top Tracks</span>
              <RefreshIcon
                color={theme === "dark" ? "white" : "black"}
                size={24}
                loading={tracksLoading}
                onClick={fetchArtistTracks}
              />
            </div>
            <div className="artist-toolbar-right">
              <span>{topTracks.length} tracks</span>
            </div>
          </div>

          <div className="artist-items-list">
            {tracksLoading ? (
              <Loading message="Loading tracks..." />
            ) : (
              topTracks.map((t, index) => (
                <div key={t.id} className="artist-track-row" draggable>
                  <div className="track-index">{index + 1}</div>
                  <TrackModel track={t} isSelected={false} />
                </div>
              ))
            )}
          </div>
        </div>

        {/* Right Column - Albums */}
        <div className="artist-column artist-column-right">
          <div className="artist-toolbar">
            <div className="artist-toolbar-left">
              <span>Albums</span>
              <RefreshIcon
                color={theme === "dark" ? "white" : "black"}
                size={24}
                loading={albumsLoading}
                onClick={fetchArtistAlbums}
              />
            </div>
            <div className="artist-toolbar-right">
              <div className="artist-filter-checkboxes">
                <label className="filter-checkbox">
                  <input
                    type="checkbox"
                    checked={filters.album}
                    onChange={() => handleFilterChange("album")}
                  />
                  <span className="checkbox-custom"></span>
                  <span className="filter-label">Albums</span>
                </label>
                <label className="filter-checkbox">
                  <input
                    type="checkbox"
                    checked={filters.single}
                    onChange={() => handleFilterChange("single")}
                  />
                  <span className="checkbox-custom"></span>
                  <span className="filter-label">Singles</span>
                </label>
                <label className="filter-checkbox">
                  <input
                    type="checkbox"
                    checked={filters.compilation}
                    onChange={() => handleFilterChange("compilation")}
                  />
                  <span className="checkbox-custom"></span>
                  <span className="filter-label">Compilations</span>
                </label>
                <label className="filter-checkbox">
                  <input
                    type="checkbox"
                    checked={filters.appears_on}
                    onChange={() => handleFilterChange("appears_on")}
                  />
                  <span className="checkbox-custom"></span>
                  <span className="filter-label">Appears On</span>
                </label>
              </div>
            </div>
          </div>

          <div className="artist-items-list">
            {albumsLoading ? (
              <Loading message="Loading albums..." />
            ) : (
              filteredAlbums.map((album) => (
                <div key={album.id} className="artist-album-row">
                  <AlbumModel album={album} isSelected={false} />
                </div>
              ))
            )}
          </div>
        </div>
      </div>
    </div>
  );
}
