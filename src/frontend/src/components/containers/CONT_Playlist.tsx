import React, { useState, useEffect } from "react";
import "./CONT_Playlist.css";
import Loading from "../ui/elements/Loading.tsx";
import TrackModel from "./items/ITEM_Track.tsx";
import { useDrop } from "react-dnd";
import { ItemTypes } from "../../utils/constants/index.ts";
import { PlaylistType, TrackType } from "../../utils/types/ModelTypes.ts";
import { getPlaylistTracks } from "../../api/API_Playlist.js";
import RefreshIcon from "../ui/icons/RefreshIcon.tsx";
import { useTheme } from "../../utils/theme/ThemeContext.tsx";

export default function PlaylistContainer({
  playlist,
}: {
  playlist: PlaylistType;
}) {
  const [pub, setPub] = useState(playlist.isPublic ?? true);
  const [collab, setCollab] = useState(playlist.isCollaborative ?? false);
  const [tracksState, setTracksState] = useState<TrackType[]>(
    playlist.tracks ?? []
  );
  const [selectedTrackId, setSelectedTrackId] = useState<string | null>(null);
  const [loading, setLoading] = useState(!playlist.tracks);
  const [tracksLoading, setTracksLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const { theme } = useTheme();
  // Fetch tracks only if they weren't passed in
  useEffect(() => {
    fetchTracks();
    // eslint-disable-next-line
  }, [playlist]);
  const fetchTracks = async () => {
    try {
      if (playlist.tracks && playlist.tracks.length > 0) return;
      setTracksLoading(true);
      setError(null);

      const res = await getPlaylistTracks(playlist.id, {
        total: playlist.length,
      });
      if (!res) throw new Error("Failed to fetch playlist");

      const fetchedTracks: TrackType[] = res.tracks.map((t: any) => ({
        id: t.id,
        title: t.name,
        artist_data: t.artist_data,
        album_data: t.album_data,
        duration: t.duration_ms,
        position: t.position,
        explicit: t.explicit,
        popularity: t.popularity,
        added_at: t.added_at,
        added_by: t.added_by,
        is_local: t.is_local,
        url: t.url,
      }));
      setTracksState(fetchedTracks);
    } catch (err: any) {
      console.error("Error fetching playlist:", err);
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
        return { name: "Playlist" };
      },
      collect: (monitor) => ({
        isOver: !!monitor.isOver(),
      }),
    }),
    []
  );

  // --- RENDER ---

  if (loading) {
    return <Loading message={`Loading playlist ${playlist.name}...`} />;
  }

  if (error) {
    return <div className="playlist-error">Error: {error}</div>;
  }

  return (
    <div className="playlist-model">
      {/* Top row: cover left, metadata right */}
      <div className="playlist-top">
        <div className="playlist-cover-wrap">
          <img
            src={playlist.coverURL}
            alt={`${playlist.name} cover`}
            className="playlist-cover"
          />
        </div>

        <div className="playlist-meta">
          <div className="playlist-meta-inner">
            <div className="playlist-owner">By {playlist.ownerName}</div>
            <h2 className="playlist-title">{playlist.name}</h2>

            <div className="playlist-switches">
              <label className="switch">
                <input
                  type="checkbox"
                  checked={pub}
                  onChange={(e) => setPub(e.target.checked)}
                  aria-label="Public playlist"
                />
                <span className="slider" />
                <span className="switch-label">Public</span>
              </label>

              <label className="switch">
                <input
                  type="checkbox"
                  checked={collab}
                  onChange={(e) => setCollab(e.target.checked)}
                  aria-label="Collaborative playlist"
                />
                <span className="slider" />
                <span className="switch-label">Collaborative</span>
              </label>
            </div>

            <div className="playlist-desc">{playlist.description}</div>
          </div>
        </div>
      </div>

      {/* Second row: scrollable tracks */}
      {tracksLoading ? (
        <Loading message="Loading tracks..." />
      ) : (
        <div
          className={`playlist-tracks ${isOver ? "drag-over" : ""}`}
          ref={drop}
        >
          <div className="playlist-toolbar">
            <div className="playlist-toolbar-left">
              #
              
              <RefreshIcon
                color={theme === "dark" ? "white" : "black"}
                size={32}
                loading={tracksLoading}
                onClick={fetchTracks}
              />
            </div>
            <div className="playlist-toolbar-right">
              {/* Right tools go here */}
            </div>
          </div>


          <div className="playlist-tracks-list">
            {tracksState.map((t, index) => (
              <div
                key={t.id}
                className={`playlist-track-row ${
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
