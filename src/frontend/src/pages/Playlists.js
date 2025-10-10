import React, { useCallback, useEffect, useState } from "react";
import { useLocation } from "react-router-dom";
import PlaylistContainer from "../components/containers/CONT_Playlist.tsx";
import Header from "../components/Header.tsx";
import Library from "../components/Library.tsx";
import { getUserPlaylists } from "../api/API_CurrentUser.js";
import "./Playlists.css";
import FunctionsPanel from "../components/FunctionsPanel.tsx";
import FunctionList from "../components/FunctionItems.tsx";
import { Playlists as FunctionsPlaylists } from "../utils/functions/Functions.ts";
import { missing_file_url } from "../utils/utils.js";
export const title = "Playlists";
export const capabilities = [
  "Create",
  "Merge",
  "Analyze",
  "Create",
  "Merge",
  "Analyze",
  "Create",
  "Merge",
  "Analyze",
  "Create",
  "Merge",
  "Analyze",
];
/** TO IMPLEMENT
 * Get Playlists
 * Organize Playlists
 * Open Playlist Overlay
 * Refresh Playlist pull
 * Create Playlist
 * Merge Playlists (Union, Intersect, Difference)
 * Playlist Owners (Collaborative setting, Public/Private setting)
 * Playlist Tracks (Add, Remove, Reorder, Sort, Shuffle)
 * Playlist Tracks Analysis (Danceability, Energy, Valence, etc.)
 * Cover Image (Upload)
 * Sort by Most listened, most played, popularity,
 *
 * Design => https://docs.google.com/document/d/19Q-iybiFCSlrb7teeN5RpKyEPH_bx_qerm0bReOwWjo/edit?tab=t.lpinfoex8z49
 */
export default function Playlists() {
  const { search } = useLocation();
  const params = new URLSearchParams(search);
  const activated = params.get("cap");

  // State for selected playlist
  const [selectedPlaylist, setSelectedPlaylist] = useState(null);
  const [playlistsData, setPlaylistsData] = useState([]);
  const [loadingPlaylists, setLoadingPlaylists] = useState(true);

  /*
  FETCH PLAYLISTS
  */
  const fetchPlaylists = async () => {
    const userId = sessionStorage.getItem("userId");
    if (!userId) return;

    try {
      setLoadingPlaylists(true);
      const res = await getUserPlaylists(userId);
      const playlists = res.map((p) => ({
        id: p.id,
        name: p.name,
        coverUrl: p.img || missing_file_url,
        ownerID: p.owner.id,
        ownerName: p.owner.name,
        description: p.description,
        length: p.track_count,
        url: p.url,
        isPublic: p.public,
        isCollaborative: p.collaborative,
      }));
      setPlaylistsData(playlists);
      if (playlists.length > 0) setSelectedPlaylist(playlists[0]);
    } catch (err) {
      console.error("Error fetching user playlists", err);
    } finally {
      setLoadingPlaylists(false);
    }
  };

  useEffect(() => {
    fetchPlaylists();
  }, []);
  // Handle playlist selection
  const handlePlaylistSelect = useCallback(
    (id) => {
      const playlist = playlistsData.find((p) => p.id === id);
      if (playlist) {
        setSelectedPlaylist(playlist);
      }
    },
    [playlistsData]
  );

  // Set first playlist as selected by default if none is selected
  useEffect(() => {
    if (!selectedPlaylist && playlistsData.length > 0) {
      setSelectedPlaylist(playlistsData[0]);
    }
  }, [playlistsData, selectedPlaylist, handlePlaylistSelect]);
  // Three-column layout state
  const [left, setLeft] = useState(() => {
    const saved = Number(localStorage.getItem("pl_left"));
    return Number.isFinite(saved) && saved > 0 ? saved : 320;
  });
  const [right, setRight] = useState(() => {
    const saved = Number(localStorage.getItem("pl_right"));
    return Number.isFinite(saved) && saved > 0 ? saved : 320;
  });

  const dragRef = React.useRef(null);

  const clampSizes = (l, r) => {
    const vw = window.innerWidth;
    const maxSide = 0.5 * vw; // each side at most 50%
    const minMiddle = 480; // ensure playlist area remains usable
    const maxAllowed = Math.max(0, vw - minMiddle);
    const cl = Math.min(Math.max(240, l), Math.min(maxSide, maxAllowed));
    const cr = Math.min(
      Math.max(240, r),
      Math.min(maxSide, vw - cl - minMiddle)
    );
    return { cl, cr };
  };

  const startDragLeft = (e) => {
    e.preventDefault();
    dragRef.current = {
      type: "left",
      startX: e.clientX,
      orig: left,
      other: right,
    };
    window.addEventListener("mousemove", onDragMove);
    window.addEventListener("mouseup", stopDrag);
  };
  const startDragRight = (e) => {
    e.preventDefault();
    dragRef.current = {
      type: "right",
      startX: e.clientX,
      orig: right,
      other: left,
    };
    window.addEventListener("mousemove", onDragMove);
    window.addEventListener("mouseup", stopDrag);
  };
  const onDragMove = (e) => {
    if (!dragRef.current) return;
    const dx = e.clientX - dragRef.current.startX;
    if (dragRef.current.type === "left") {
      const nextL = dragRef.current.orig + dx;
      const { cl, cr } = clampSizes(nextL, dragRef.current.other);
      setLeft(cl);
      setRight(cr);
    } else {
      const nextR = dragRef.current.orig - dx; // dragging divider left increases right
      const { cl, cr } = clampSizes(dragRef.current.other, nextR);
      setLeft(cl);
      setRight(cr);
    }
  };
  const stopDrag = () => {
    window.removeEventListener("mousemove", onDragMove);
    window.removeEventListener("mouseup", stopDrag);
    if (dragRef.current) {
      try {
        localStorage.setItem("pl_left", String(left));
        localStorage.setItem("pl_right", String(right));
      } catch {}
    }
    dragRef.current = null;
  };

  useEffect(() => {
    const onResize = () => {
      const { cl, cr } = clampSizes(left, right);
      setLeft(cl);
      setRight(cr);
    };
    window.addEventListener("resize", onResize);
    return () => window.removeEventListener("resize", onResize);
  }, [left, right]);
  return (
    <div className="app-container">
      {activated && (
        <div
          style={{
            marginBottom: 12,
            padding: 10,
            borderRadius: 8,
            background: "rgba(29,185,84,0.15)",
            color: "var(--text)",
            border: "1px solid rgba(29,185,84,0.35)",
            fontWeight: 600,
          }}
        >
          Activated capability: {activated}
        </div>
      )}
      <Header includeLibraryButton />

      <div
        className="playlists-root"
        style={{ "--left": `${left}px`, "--right": `${right}px` }}
      >
        {/* Left: Library (default to playlists) */}
        <div className="pane pane-left">
          <div
            className="pane-divider divider-left"
            onMouseDown={startDragLeft}
          />
          <div
            style={{ height: "100%", display: "flex", flexDirection: "column" }}
          >
            <div className="functions-header">Library</div>
            <div style={{ padding: 8, flex: 1, overflow: "auto" }}>
              <Library
                defaultActive={["playlists"]}
                exclude={["tracks", "artists", "albums"]} // Hide tracks and artists, only show playlists and albums
                selectedPlaylistId={selectedPlaylist?.id}
                onPlaylistSelect={handlePlaylistSelect}
                playlistsData={playlistsData}
                loading={loadingPlaylists}
                onRefresh={fetchPlaylists}
              />
            </div>
          </div>
        </div>

        {/* Middle: Playlist model */}
        <div className="pane pane-middle">
          <div>
            {selectedPlaylist ? (
              <PlaylistContainer
                key={selectedPlaylist.id}
                id={selectedPlaylist.id}
                coverUrl={selectedPlaylist.coverUrl}
                name={selectedPlaylist.name}
                ownerName={selectedPlaylist.ownerName}
                ownerID={selectedPlaylist.ownerID}
                description={selectedPlaylist.description}
                isPublic={selectedPlaylist.isPublic}
                isCollaborative={selectedPlaylist.isCollaborative}
                length={selectedPlaylist.length}
                url={selectedPlaylist.url}
              />
            ) : (
              <div className="no-playlist-selected">
                <p>No playlist selected</p>
              </div>
            )}
          </div>
        </div>

        {/* Right: Functions panel */}
        <div className="pane pane-right">
          <div
            className="pane-divider divider-right"
            onMouseDown={startDragRight}
          />
          <FunctionsPanel title="Playlist Functions">
            <FunctionList
              groups={FunctionsPlaylists()}
              onResult={(id, res) => {
                console.log("Function result", id, res);
              }}
            />
          </FunctionsPanel>
        </div>
      </div>
    </div>
  );
}
