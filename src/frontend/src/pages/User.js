import React, { useEffect, useState } from "react";
import { useLocation } from "react-router-dom";
import Header from "../components/Header.tsx";
import { getUserProfile } from "../api/API_CurrentUser.js";
import "./User.css";
import FunctionsPanel from "../components/FunctionsPanel.tsx";
import FunctionList from "../components/FunctionItems.tsx";
import { User as FunctionsUser } from "../utils/functions/Functions.ts";
import { missing_file_url } from "../utils/utils.js";
export const title = "User";
export const capabilities = [];
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

  // Three-column layout state
  const [left, setLeft] = useState(() => {
    const saved = Number(localStorage.getItem("pl_left"));
    if (Number.isFinite(saved) && saved > 0) return saved;

    // default to half viewport width minus gap
    const vw = window.innerWidth;
    return Math.floor(vw / 2 - vw / 80 - 6); // 6 = half of 12px gap
  });
  const [right, setRight] = useState(() => {
    const saved = Number(localStorage.getItem("pl_right"));
    if (Number.isFinite(saved) && saved > 0) return saved;

    const vw = window.innerWidth;
    return Math.floor(vw / 2 - vw / 80 - 6);
  });
  const dragRef = React.useRef(null);

  const clampSizes = (l, r) => {
    const vw = window.innerWidth - 60;
    const maxSide = 0.8 * vw; // At most .7 of vw
    const minSide = vw-maxSide
    console.log(vw)

    const cl = Math.min(Math.max(minSide, l), maxSide);
    const cr = Math.min(Math.max(minSide, r), maxSide);

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
    const dx = e.clientX - dragRef.current.startX; //e.clientX == currentMousePosition, dragRef.current.startX = Starting Position; dx = total move
    if (dragRef.current.type === "left") {
      console.log(dragRef.current.other)
      console.log(dragRef.current.startX)
      console.log("total", dragRef.current.startX+dragRef.current.other)

      const nextL = dragRef.current.orig + dx;
      const { cl, cr } = clampSizes(nextL, dragRef.current.other - dx);
      setLeft(cl);
      setRight(cr);
    } else {
      const nextR = dragRef.current.orig - dx; // dragging divider left increases right
      const { cl, cr } = clampSizes( dragRef.current.other + dx, nextR);
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
      <Header />

      <div
        className="user-root"
        style={{ "--left": `${left}px`, "--right": `${right}px` }}
      >
        {/* Left: User Info*/}
        <div className="pane pane-left">
          <div
            className="pane-divider divider-left"
            onMouseDown={startDragLeft}
          />
          <div
            style={{ height: "100%", display: "flex", flexDirection: "column" }}
          >
            <div className="functions-header">User</div>
            <div style={{ padding: 8, flex: 1, overflow: "auto" }}></div>
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
              groups={FunctionsUser()}
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
