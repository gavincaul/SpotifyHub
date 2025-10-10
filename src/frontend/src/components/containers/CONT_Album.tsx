import React, { useState, useEffect } from "react";
import "./CONT_Album.css";
import Loading from "../ui/elements/Loading.tsx";
import TrackModel from "./items/ITEM_Track.tsx";
import { useDrop } from "react-dnd";
import { ItemTypes } from "../../utils/constants/index.ts";
import { AlbumType, TrackType } from "../../utils/types/ModelTypes.ts";
import { getAlbumTracks } from "../../api/API_Album.js";
import RefreshIcon from "../ui/icons/RefreshIcon.tsx";
import { useTheme } from "../../utils/theme/ThemeContext.tsx";

export default function AlbumContainer({ album }: { album: AlbumType }) {
  const [tracksState, setTracksState] = useState<TrackType[]>(
    album.tracks ?? []
  );
  const [selectedTrackId, setSelectedTrackId] = useState<string | null>(null);
  const [loading, setLoading] = useState(!album.tracks);
  const [tracksLoading, setTracksLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const { theme } = useTheme();
  // Fetch tracks only if they weren't passed in
  useEffect(() => {
    fetchTracks();
    // eslint-disable-next-line
  }, [album]);
  const fetchTracks = async () => {
    try {
      if (album.tracks && album.tracks.length > 0) return;
      setTracksLoading(true);
      setError(null);

      const res = await getAlbumTracks(album.id);
      if (!res) throw new Error("Failed to fetch album");

      const fetchedTracks: TrackType[] = res.map((t: any) => ({
        id: t.id,
        name: t.name,
        artist_data: t.artist_data,
        album_data: t.album_data,
        duration: t.duration,
        position: t.position,
        explicit: t.explicit,
        popularity: t.popularity,
        added_at: t.added_at,
        added_by: t.added_by,
        is_local: t.is_local,
        url: t.url,
        isSelected: false,
      }));

      setTracksState(fetchedTracks);
    } catch (err: any) {
      console.error("Error fetching album:", err);
      setError(err.message || "Unexpected error");
    } finally {
      setTracksLoading(false);
      setLoading(false);
    }
  };

  const [{ isOver }, drop] = useDrop(
    () => ({
      accept: ItemTypes.TRACK,
      drop: (item: { id: string; type: string }) => {
        console.log("Dropped track:", item.id);
        return { name: "album" };
      },
      collect: (monitor) => ({
        isOver: !!monitor.isOver(),
      }),
    }),
    []
  );

  // --- RENDER ---

  if (loading) {
    return <Loading message={`Loading album ${album.name}...`} />;
  }

  if (error) {
    return <div className="album-error">Error: {error}</div>;
  }

  return (
    <div className="album-model">
      {/* Top row: cover left, metadata right */}
      <div className="album-top">
        <div className="album-cover-wrap">
          <img
            src={album.images.large}
            alt={`${album.name} cover`}
            className="album-cover"
          />
        </div>

        <div className="album-meta">
          <div className="album-meta-inner">
            <div className="album-owner">
              By {album.artists.map((a) => a.name + ", ")}
            </div>
            <h2 className="album-title">{album.name}</h2>

            <div className="album-desc">{album.total_tracks}</div>
          </div>
        </div>
      </div>

      {/* Second row: scrollable tracks */}
      {tracksLoading ? (
        <Loading message="Loading tracks..." />
      ) : (
        <div className={`album-tracks ${isOver ? "drag-over" : ""}`} ref={drop}>
          <div className="album-toolbar">
            <div className="album-toolbar-left">
              #
              <RefreshIcon
                color={theme === "dark" ? "white" : "black"}
                size={32}
                loading={tracksLoading}
                onClick={fetchTracks}
              />
            </div>
            <div className="album-toolbar-right">
              {/* Right tools go here */}
            </div>
          </div>

          <div className="album-tracks-list">
            {tracksState.map((t, index) => (
              <div
                key={t.id}
                className={`album-track-row ${
                  selectedTrackId === t.id ? "selected" : ""
                }`}
                onClick={() => setSelectedTrackId(t.id)}
                draggable
              >
                <div className="track-index">{index + 1}</div>
                <TrackModel track={t} isSelected={selectedTrackId === t.id} />
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}
