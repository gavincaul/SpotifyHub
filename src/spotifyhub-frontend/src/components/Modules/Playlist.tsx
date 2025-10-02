import React, { useMemo, useState, useCallback } from "react";
import "./Playlist.css";
import TrackModel from "./Models/TrackModel.tsx";
import { useDrop } from "react-dnd";
import { ItemTypes } from "../../constants/index.ts";

export interface Track {
  id: string;
  title: string;
  artist: string;
  album: string;
  albumArt: string;
  duration: number; // Changed from durationMs to match TrackModelProps
  playCount?: number;
  releaseDate?: string;
  bpm?: number;
  key?: string;
  isSelected?: boolean;
  onClick?: (id: string) => void;
}

type PlaylistProps = {
  coverUrl?: string;
  name?: string;
  owner?: string;
  description?: string;
  isPublic?: boolean;
  isCollaborative?: boolean;
  tracks?: Track[];
  onTrackClick?: (trackId: string) => void;
  onTracksReordered?: (tracks: Track[]) => void;
};

// Time formatting is now handled in TrackModel component
const mockTracks = (n = 18): Track[] =>
  Array.from({ length: n }).map((_, i) => {
    const artist = ["Ava Night", "Neon Waves", "The Loops", "Cobalt Sky"][
      i % 4
    ];
    const album = `Album ${Math.floor(i / 4) + 1}`;
    const duration = 120 + (i % 5) * 23; // In seconds for TrackModel

    return {
      id: `t-${i}`,
      title: `Track ${i + 1}`,
      artist,
      album,
      albumArt: `https://picsum.photos/seed/album-${i}-${encodeURIComponent(
        album
      )}/200/200`,
      duration,
      playCount: Math.floor(Math.random() * 10000),
      releaseDate: new Date(Date.now() - Math.random() * 31536000000)
        .toISOString()
        .split("T")[0],
      bpm: [120, 125, 128, 130, 140][i % 5],
      key: ["C#m", "Dm", "Em", "F#m", "Gm"][i % 5],
    };
  });

export default function Playlist({
  //Change to playlist ID
  coverUrl,
  name,
  owner,
  description,
  isPublic,
  isCollaborative,
  tracks,
}: PlaylistProps) {
  const playlistName = useMemo(() => name ?? "My Playlist", [name]);
  const playlistOwner = useMemo(() => owner ?? "You", [owner]);
  const playlistCover = useMemo(
    () =>
      coverUrl ??
      `https://picsum.photos/seed/${encodeURIComponent(playlistName)}/600/600`,
    [coverUrl, playlistName]
  );
  const playlistDesc = useMemo(
    () => description ?? "Add a short description for your playlist.",
    [description]
  );
  const playlistTracks = useMemo(() => tracks ?? mockTracks(24), [tracks]);

  const [pub, setPub] = useState(isPublic ?? true);
  const [collab, setCollab] = useState(isCollaborative ?? false);
  const [tracksState] = useState(playlistTracks);
  const [selectedTrackId, setSelectedTrackId] = useState(null as string | null);

  const handleTrackClick = useCallback((id: string) => {
    setSelectedTrackId((prevId) => (prevId === id ? null : id));
  }, []);

  const [{ isOver }, drop] = useDrop(
    () => ({
      accept: ItemTypes.TRACK,
      drop: (item: { id: string; type: string }, monitor) => {
        // Handle the drop - in a real app, this would update the playlist order
        console.log("Dropped track:", item.id);
        return { name: "Playlist" };
      },
      collect: (monitor) => ({
        isOver: !!monitor.isOver(),
      }),
    }),
    []
  );

  return (
    <div className="playlist-model">
      {/* Top row: cover left, metadata right (height capped to image) */}
      <div className="playlist-top">
        <div className="playlist-cover-wrap">
          <img
            src={playlistCover}
            alt={`${playlistName} cover`}
            className="playlist-cover"
          />
        </div>

        <div className="playlist-meta">
          <div className="playlist-meta-inner">
            <div className="playlist-owner">By {playlistOwner}</div>
            <h2 className="playlist-title">{playlistName}</h2>

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

            <div className="playlist-desc">{playlistDesc}</div>
          </div>
        </div>
      </div>

      {/* Second row: scrollable tracks */}
      <div
        className={`playlist-tracks ${isOver ? "drag-over" : ""}`}
        ref={drop}
        style={{
          outline: isOver ? "2px dashed var(--accent)" : "none",
          borderRadius: "4px",
          transition: "outline 0.2s ease",
        }}
      >
        <div className="playlist-tracks-header">
          <div className="th th-idx">#</div>
          <div className="th th-title">Title</div>
          <div className="th th-album">Album</div>
          <div className="th th-time">Time</div>
          <div className="th th-playcount">Playcount</div>
          <div className="th th-release-date">Release Date</div>
        </div>
        <div className="playlist-tracks-list">
          {tracksState.map((track, index) => (
            <div
              key={track.id}
              className="track-row"
              draggable
              onDragStart={(e) => {
                e.dataTransfer.setData(
                  "application/json",
                  JSON.stringify({ id: track.id, type: "track" })
                );
                e.dataTransfer.effectAllowed = "move";
              }}
            >
              <div className="td td-idx">{index + 1}</div>
              <TrackModel
                id={track.id}
                albumArt={track.albumArt}
                title={track.title}
                artist={track.artist}
                album={track.album}
                duration={track.duration}
                playCount={track.playCount}
                releaseDate={track.releaseDate}
                isSelected={selectedTrackId === track.id}
                onClick={handleTrackClick}
              />
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
