import React, { useEffect, useMemo, useRef, useState } from "react";
import ReactDOM from "react-dom";
import "./AlbumModule.css";
import TrackModel from "./Models/TrackModel.tsx";

type AlbumProps = {
  title?: string;
  artist?: string;
  coverUrl?: string;
  tracks?: typeof TrackModel[];
  onOpen?: (album: { title: string; artist: string }) => void;
  onTrackClick?: (trackTitle: string, trackIndex: number) => void;
  onArtistClick?: (artist: string) => void;
  relatedAlbums?: { title?: string; artist?: string; coverUrl?: string; tracks?: string[] }[];
  variant?: "default" | "small";
  openInStack?: boolean; // when true, render overlay via portal so it's a separate top-level overlay
};

// ------------------------------
// Mock data generation helpers
// Used only when props are not provided, so the component can render standalone
// ------------------------------
const adjectives = [
  "Electric",
  "Golden",
  "Midnight",
  "Neon",
  "Crimson",
  "Velvet",
  "Wandering",
  "Silent",
  "Fading",
  "Echoing",
];
const nouns = [
  "Dreams",
  "Horizons",
  "Lights",
  "Skies",
  "Reflections",
  "Waves",
  "Whispers",
  "Embers",
  "Shadows",
  "Stories",
];
const names = [
  "Ava Night",
  "Liam Stone",
  "Noah Rivers",
  "Mia Hart",
  "Zoe Lake",
  "Eli North",
  "Ivy Rose",
  "Levi Quinn",
  "Nova Rae",
  "Kai West",
];

function randomFrom<T>(arr: T[]): T {
  return arr[Math.floor(Math.random() * arr.length)];
}

function genTitle() {
  return `${randomFrom(adjectives)} ${randomFrom(nouns)}`;
}

function genArtist() {
  return randomFrom(names);
}

function genTracks(count = 10) {
  const tracks: string[] = [];
  for (let i = 1; i <= count; i++) {
    tracks.push(`${randomFrom(adjectives)} ${randomFrom(nouns)} ${i}`);
  }
  return tracks;
}

/**
 * End of random gen
 * 
 */

export const Album = ({
  title,
  artist,
  coverUrl,
  tracks,
  onOpen,
  onTrackClick,
  onArtistClick,
  relatedAlbums,
  variant = "default",
  openInStack = false,
}: AlbumProps) => {
  const [open, setOpen] = useState(false);
  const [origin, setOrigin] = useState(null);
  const cardRef = useRef(null);
  const [pos, setPos] = useState<{ x: number; y: number } | null>(null);
  const [size, setSize] = useState<{ width: number; height: number } | null>(null);
  const dragState = useRef<any>(null);
  const resizeState = useRef<any>(null);
  // z-index management so the most recently interacted modal comes to the front
  // Module-level counter
  // eslint-disable-next-line @typescript-eslint/no-unused-vars
  const zCounter = (Album as any)._zCounter || 1000;
  (Album as any)._zCounter = zCounter; // ensure exists
  const nextZ = () => {
    (Album as any)._zCounter = ((Album as any)._zCounter || 1000) + 1;
    return (Album as any)._zCounter;
  };
  const [zIndex, setZIndex] = useState<number>(nextZ());

  const albumTitle = useMemo(() => title ?? genTitle(), [title]);
  const albumArtist = useMemo(() => artist ?? genArtist(), [artist]);
  const albumCover = useMemo(
    () => coverUrl ?? `https://picsum.photos/seed/${encodeURIComponent(albumTitle)}/400/400`,
    [coverUrl, albumTitle]
  );
  const albumTracks = useMemo(() => tracks ?? genTracks(12), [tracks]);
  const related = useMemo(() => {
    if (relatedAlbums && relatedAlbums.length) return relatedAlbums;
    // generate 6 mock related albums by same artist for now
    return Array.from({ length: 6 }).map(() => ({
      title: genTitle(),
      artist: albumArtist,
      coverUrl: `https://picsum.photos/seed/${encodeURIComponent(genTitle())}/300/300`,
      tracks: genTracks(8),
    }));
  }, [relatedAlbums, albumArtist]);

  const openModal = () => {
    // Compute card center as a percentage of viewport to use for transform-origin
    if (cardRef.current) {
      const rect = cardRef.current.getBoundingClientRect();
      const cx = rect.left + rect.width / 2;
      const cy = rect.top + rect.height / 2;
      const xPct = (cx / window.innerWidth) * 100;
      const yPct = (cy / window.innerHeight) * 100;
      setOrigin({ xPct, yPct });
    }
    
    setOpen(true);
    setZIndex(nextZ());
    // Initialize position and size to center of viewport with a reasonable default
    const defaultWidth = Math.min(720, Math.round(window.innerWidth * 0.92));
    const defaultHeight = Math.min(520, Math.round(window.innerHeight * 0.8));
    const startX = Math.max(0, Math.round(window.innerWidth / 2 - defaultWidth / 2));
    const startY = Math.max(0, Math.round(window.innerHeight / 2 - defaultHeight / 2));
    setPos({ x: startX, y: startY });
    setSize({ width: defaultWidth, height: defaultHeight });
    onOpen?.({ title: albumTitle, artist: albumArtist });
  };

  const closeModal = () => setOpen(false);

  const handleKeyDown = (e: any) => {
    if (e.key === "Enter" || e.key === " ") {
      e.preventDefault();
      openModal();
    }
  };

  // Drag handlers
  const onHeaderMouseDown = (e: any) => {
    // bring to front on interaction
    setZIndex(nextZ());
    if (!pos || !size) return;
    e.preventDefault();
    dragState.current = {
      startX: e.clientX,
      startY: e.clientY,
      origX: pos.x,
      origY: pos.y,
    };
    window.addEventListener("mousemove", onHeaderMouseMove as any);
    window.addEventListener("mouseup", onHeaderMouseUp as any);
  };

  const onHeaderMouseMove = (e: MouseEvent) => {
    if (!dragState.current || !size) return;
    const dx = e.clientX - dragState.current.startX;
    const dy = e.clientY - dragState.current.startY;
    let nx = dragState.current.origX + dx;
    let ny = dragState.current.origY + dy;
    // Constrain within viewport
    nx = Math.max(0, Math.min(nx, window.innerWidth - size.width));
    ny = Math.max(0, Math.min(ny, window.innerHeight - size.height));
    setPos({ x: nx, y: ny });
  };

  const onHeaderMouseUp = () => {
    dragState.current = null;
    window.removeEventListener("mousemove", onHeaderMouseMove as any);
    window.removeEventListener("mouseup", onHeaderMouseUp as any);
  };

  // Resize handlers (bottom-right corner)
  const onResizeMouseDown = (e: any) => {
    if (!pos || !size) return;
    e.preventDefault();
    resizeState.current = {
      startX: e.clientX,
      startY: e.clientY,
      origW: size.width,
      origH: size.height,
    };
    window.addEventListener("mousemove", onResizeMouseMove as any);
    window.addEventListener("mouseup", onResizeMouseUp as any);
  };

  const onResizeMouseMove = (e: MouseEvent) => {
    if (!resizeState.current || !pos) return;
    let nw = resizeState.current.origW + (e.clientX - resizeState.current.startX);
    let nh = resizeState.current.origH + (e.clientY - resizeState.current.startY);
    // Min size and max to viewport
    const minW = 360;
    const minH = 260;
    nw = Math.max(minW, Math.min(nw, window.innerWidth - pos.x));
    nh = Math.max(minH, Math.min(nh, window.innerHeight - pos.y));
    setSize({ width: Math.round(nw), height: Math.round(nh) });
  };

  const onResizeMouseUp = () => {
    resizeState.current = null;
    window.removeEventListener("mousemove", onResizeMouseMove as any);
    window.removeEventListener("mouseup", onResizeMouseUp as any);
  };

  // Cleanup listeners on unmount just in case
  useEffect(() => {
    return () => {
      window.removeEventListener("mousemove", onHeaderMouseMove as any);
      window.removeEventListener("mouseup", onHeaderMouseUp as any);
      window.removeEventListener("mousemove", onResizeMouseMove as any);
      window.removeEventListener("mouseup", onResizeMouseUp as any);
    };
  }, []);

  const wrapperClass = variant === "small" ? "album-wrapper album-wrapper--small" : "album-wrapper";

  return (
    <div className={wrapperClass}>
      <div
        role="button"
        tabIndex={0}
        aria-label={`Open album ${albumTitle} by ${albumArtist}`}
        onClick={openModal}
        onKeyDown={handleKeyDown}
        className="album-card"
        ref={cardRef}
      >
        <img src={albumCover} alt={`${albumTitle} cover`} className="album-cover" />
        <div className="album-meta">
          <div className="album-title">{albumTitle}</div>
          <button
            type="button"
            className="album-artist album-artist-link"
            onClick={() => (onArtistClick ? onArtistClick(albumArtist) : console.log("artist clicked", albumArtist))}
          >
            {albumArtist}
          </button>
        </div>
      </div>

      {open && (() => {
        const modal = (
          <div
            role="dialog"
            aria-modal="true"
            aria-labelledby="album-modal-title"
            className="album-modal-overlay album-modal-opening"
            style={origin ? ({
              ["--origin-x"]: `${origin.xPct}%`,
              ["--origin-y"]: `${origin.yPct}%`,
              zIndex: zIndex,
            } as any) : ({ zIndex } as any)}
          >
            <div
              className="album-modal"
              style={pos && size ? ({ left: pos.x, top: pos.y, width: size.width, height: size.height, position: "absolute" } as any) : undefined}
            >
              <div className="album-modal-header" onMouseDown={onHeaderMouseDown} style={{ cursor: "move" }}>
                <div id="album-modal-title" className="album-modal-title">
                  {albumTitle} — {albumArtist}
                </div>
                <button onClick={closeModal} className="album-close-btn" aria-label="Close album">
                  ×
                </button>
              </div>
              <div className="album-modal-body">
                <div className="album-modal-cover-wrap">
                  <img src={albumCover} alt={`${albumTitle} cover`} className="album-modal-cover" />
                  <div className="album-related">
                    <div className="album-related-title">Other albums by {albumArtist}</div>
                    <div className="album-related-row">
                      {related.map((a, idx) => (
                        <div key={`${a.title}-${idx}`} className="album-related-item">
                          <Album
                            title={a.title}
                            artist={a.artist}
                            coverUrl={a.coverUrl}
                            tracks={a.tracks}
                            variant="small"
                            openInStack={true}
                          />
                        </div>
                      ))}
                    </div>
                  </div>
                </div>
                <ul className="album-track-list">
                  {albumTracks.map((t, i) => (
                    <li key={`${t}-${i}`} className="album-track-item">
                      <button
                        className="album-track-btn"
                        onClick={() => onTrackClick ? onTrackClick(t, i) : console.log("track clicked", t)}
                      >
                        {i + 1}. {t}
                      </button>
                    </li>
                  ))}
                </ul>
                <div className="album-resize-handle" onMouseDown={onResizeMouseDown} />
              </div>
            </div>
          </div>
        );
        return openInStack ? ReactDOM.createPortal(modal, document.body) : modal;
      })()}
    </div>
  );
};

export default Album;

