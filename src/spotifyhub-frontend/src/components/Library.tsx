import React, { useMemo, useState } from "react";
// Navigation is handled by parent component
import "./Library.css";
import PlaylistModel from "./Modules/Models/PlaylistModel.tsx";

export type LibraryContentType = "albums" | "playlists" | "tracks" | "artists";

export type LibraryProps = {
  defaultActive?: LibraryContentType[];
  exclude?: LibraryContentType[];
  selectedPlaylistId?: string | null;
  onPlaylistSelect?: (id: string) => void;
  playlistsData?: Array<{
    id: string;
    name: string;
    owner: string;
    description?: string;
    coverUrl?: string;
    length?: string;
    isPublic?: boolean;
    isCollaborative?: boolean;
  }>;
};

const ALL_CONTENT_TYPES: LibraryContentType[] = ["albums", "playlists", "tracks", "artists"];

export default function Library({
  defaultActive = ["albums", "playlists"],
  exclude = [],
  selectedPlaylistId,
  onPlaylistSelect,
  playlistsData: externalPlaylistsData = [],
}: LibraryProps) {
  const [active, setActive] = useState<Record<string, boolean>>(() => {
    const base: Record<string, boolean> = {};
    ALL_CONTENT_TYPES
      .filter(type => !exclude.includes(type))
      .forEach((k) => {
        base[k] = defaultActive.includes(k);
      });
    return base;
  });
  const [order, setOrder] = useState<string[]>(
    () => ALL_CONTENT_TYPES.filter(type => !exclude.includes(type)) as unknown as string[]
  );
  const [dragKey, setDragKey] = useState<string | null>(null);

  const toggles = useMemo(
    () => ALL_CONTENT_TYPES
      .filter(type => !exclude.includes(type))
      .map((k) => ({ key: k, label: k[0].toUpperCase() + k.slice(1) })),
    [exclude]
  );
  const activeKeys = order.filter((k) => active[k]);

  const onToggle = (key: string) =>
    setActive((prev) => ({ ...prev, [key]: !prev[key] }));

  // DnD handlers for inner columns
  const onColDragStart = (key: string) => (e: any) => {
    setDragKey(key);
    e.dataTransfer.effectAllowed = "move";
    try {
      e.dataTransfer.setData("text/plain", key);
    } catch {}
  };

  const onColDragOver = (overKey: string) => (e: any) => {
    e.preventDefault(); // allow drop
    if (!dragKey || dragKey === overKey) return;
  };

  const onColDrop = (overKey: string) => (e: any) => {
    e.preventDefault();
    const from = dragKey;
    setDragKey(null);
    if (!from || from === overKey) return;
    setOrder((prev) => {
      const list = prev.slice();
      const fromIdx = list.indexOf(from);
      const toIdx = list.indexOf(overKey);
      if (fromIdx === -1 || toIdx === -1) return prev;
      list.splice(fromIdx, 1);
      list.splice(toIdx, 0, from);
      return list;
    });
  };

  // Use external playlists data if provided, otherwise use sample data
  const playlistsData = useMemo(() => {
    if (externalPlaylistsData && externalPlaylistsData.length > 0) {
      return externalPlaylistsData.map(p => ({
        id: p.id,
        imageUrl: p.coverUrl || `https://picsum.photos/seed/${p.id}/200/200`,
        name: p.name,
        length: p.length || "0 songs",
        owner: p.owner || "You",
      }));
    }
    
    // Fallback sample data
    return [
      {
        id: "pl_1",
        imageUrl: "https://picsum.photos/seed/playlist1/200/200",
        name: "Focus Flow",
        length: "48 songs",
        owner: "You",
      },
      {
        id: "pl_2",
        imageUrl: "https://picsum.photos/seed/playlist2/200/200",
        name: "Gym Hype",
        length: "36 songs",
        owner: "You",
      },
      {
        id: "pl_3",
        imageUrl: "https://picsum.photos/seed/playlist3/200/200",
        name: "Chill Vibes",
        length: "64 songs",
        owner: "You",
      },
    ];
  }, [externalPlaylistsData]);

  return (
    <div className="library">
      <div className="library-content">
        <div className="library-actions">
          {toggles.map(({ key, label }) => (
            <button
              key={key}
              className={"library-action-btn" + (active[key] ? " active" : "")}
              onClick={() => onToggle(key)}
            >
              {label}
            </button>
          ))}
        </div>

        <div className="library-content-cols">
          {activeKeys.map((k) => (
            <div
              key={k}
              className={"library-col" + (dragKey === k ? " dragging" : "")}
              draggable
              onDragStart={onColDragStart(k)}
              onDragOver={onColDragOver(k)}
              onDrop={onColDrop(k)}
            >
              <div className="library-col-header">
                {k[0].toUpperCase() + k.slice(1)}
              </div>
              <div className="library-col-body">
                {k === "playlists" ? (
                  <div style={{ display: "grid", gap: 8 }}>
                    {playlistsData.map((p) => (
                      <div key={p.id}>
                        <div 
                          className={`playlist-item ${selectedPlaylistId === p.id ? 'selected' : ''}`}
                          onClick={() => onPlaylistSelect?.(p.id)}
                        >
                          <PlaylistModel
                            id={p.id}
                            imageUrl={p.imageUrl}
                            name={p.name}
                            length={p.length}
                            owner={p.owner}
                            onOpen={onPlaylistSelect}
                          />
                        </div>
                      </div>
                    ))}
                  </div>
                ) : (
                  <ul style={{ margin: 0, padding: 0, listStyle: "none" }}>
                    {Array.from({ length: 12 }).map((_, i) => (
                      <li
                        key={i}
                        style={{
                          padding: "6px 0",
                          borderBottom: "1px solid var(--muted)",
                        }}
                      >
                        {k} item {i + 1}
                      </li>
                    ))}
                  </ul>
                )}
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
