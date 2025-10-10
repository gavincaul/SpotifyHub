import React, { useCallback, useEffect, useState } from "react";
import Header from "../components/Header.tsx";
import PlaylistContainer from "../components/containers/CONT_Playlist.tsx";
import AlbumContainer from "../components/containers/CONT_Album.tsx"
import TrackContainer from "../components/containers/CONT_Track.tsx"
import ArtistContainer from "../components/containers/CONT_Artist.tsx"
import FunctionsPanel from "../components/FunctionsPanel.tsx";
import FunctionList from "../components/FunctionItems.tsx";
import { Library as LibraryFunctions } from "../utils/functions/Functions.ts";
import LibraryComponent from "../components/Library.tsx";
import {
  getUserLibrary,
  getUserPlaylists,
  getUserAlbums,
  getUserTracks,
  getUserArtists,
} from "../api/API_CurrentUser.js";
import "./Library.css";
export const title = "Your Library";
export const capabilities = ["Liked Songs", "Albums", "Artists"];
export default function Library() {
  const [selectedItem, setSelectedItem] = useState(null);

  const [libraryData, setLibraryData] = useState({
    playlists: [],
    albums: [],
    tracks: [],
    artists: [],
  });

  const [loading, setLoading] = useState({
    playlists: false,
    albums: false,
    tracks: false,
    artists: false,
  });

  // fetch all types on mount
  useEffect(() => {
    fetchLibraryData();
  }, []);

  const fetchLibraryData = useCallback(async () => {
    try {
      setLoading({
        playlists: true,
        albums: true,
        tracks: true,
        artists: true,
      });
      const res = await getUserLibrary();
      setLibraryData({
        playlists: res.playlists,
        albums: res.albums,
        tracks: res.tracks,
        artists: res.artists,
      });
    } catch (err) {
      console.error("Error fetching library data", err);
    } finally {
      setLoading({
        playlists: false,
        albums: false,
        tracks: false,
        artists: false,
      });
    }
  }, []);

  // refresh individual type
  const refreshType = async (type) => {
    try {
      setLoading((prev) => ({ ...prev, [type]: true }));

      let data = [];
      switch (type) {
        case "playlists":
          data = await getUserPlaylists();
          break;
        case "albums":
          data = await getUserAlbums();
          break;
        case "tracks":
          data = await getUserTracks();
          break;
        case "artists":
          data = await getUserArtists();
          break;
        default:
          break;
      }

      setLibraryData((prev) => ({ ...prev, [type]: data }));
    } catch (err) {
      console.error(`Failed to refresh ${type}`, err);
    } finally {
      setLoading((prev) => ({ ...prev, [type]: false }));
    }
  };

  /* DRAG n' DROP
   */
  const [left, setLeft] = useState(() => {
    const saved = Number(localStorage.getItem("pl_left"));
    return Number.isFinite(saved) && saved > 0 ? saved : 820;
  });
  const [right, setRight] = useState(() => {
    const saved = Number(localStorage.getItem("pl_right"));
    return Number.isFinite(saved) && saved > 0 ? saved : 320;
  });

  const dragRef = React.useRef(null);
  const clampSizes = (l, r) => {
    const vw = window.innerWidth;
    const maxSide = selectedItem ? 0.5 * vw : 0.8 * vw; // each side at most 50%
    const minMiddle = selectedItem ? 480 : 0; // if no middle, middle width is 0
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
      <Header includeLibraryButton />
      <div
        className={`library-root ${!selectedItem ? "no-middle" : ""}`}
        style={{ "--left": `${left}px`, "--right": `${right}px` }}
      >
        {/* Left: Library */}
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
              <LibraryComponent
                libraryData={libraryData}
                loading={loading}
                onItemSelect={(item, type) => setSelectedItem({ item, type })}
                onRefresh={refreshType}
              />
            </div>
          </div>
        </div>
        {selectedItem && (
          <div className="pane pane-middle">
            {selectedItem.type === "playlists" && (
              <PlaylistContainer playlist={selectedItem.item} />
            )}
            {selectedItem.type === "albums" && (
              <AlbumContainer album={selectedItem.item} />
            )}
            {selectedItem.type === "artists" && (
              <ArtistContainer artist={selectedItem.item} />
            )}
            {selectedItem.type === "tracks" && (
              <TrackContainer track={selectedItem.item} />
            )}
          </div>
        )}

        <div className="pane pane-right">
          {selectedItem && (
            <div
              className="pane-divider divider-right"
              onMouseDown={startDragRight}
            />
          )}
          <FunctionsPanel title="Library Functions">
            <FunctionList
              groups={LibraryFunctions()}
              onResult={(id, res) => console.log("Function result", id, res)}
            />
          </FunctionsPanel>
        </div>
      </div>
    </div>
  );
}
