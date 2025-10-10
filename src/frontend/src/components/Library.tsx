import React, { useMemo, useState } from "react";
import "./Library.css";
import { useTheme } from "../utils/theme/ThemeContext.tsx";
import Loading from "./ui/elements/Loading.tsx";
import RefreshIcon from "./ui/icons/RefreshIcon.tsx";

import {
  LibraryData,
  PlaylistType,
  AlbumType,
  ArtistType,
  TrackType,
} from "../utils/types/ModelTypes.ts";
import AlbumItem from "./containers/items/ITEM_Album.tsx";
import TrackItem from "./containers/items/ITEM_Track.tsx";
import PlaylistItem from "./containers/items/ITEM_Playlist.tsx";
import ArtistItem from "./containers/items/ITEM_Artist.tsx";

export type LibraryContentType = "albums" | "playlists" | "tracks" | "artists";

export interface LibraryProps {
  defaultActive?: LibraryContentType[];
  exclude?: LibraryContentType[];
  onItemSelect?: (
    item: PlaylistType | AlbumType | TrackType | ArtistType,
    type: LibraryContentType
  ) => void;
  libraryData?: LibraryData;
  loading: Record<LibraryContentType, boolean>;
  onRefresh?: (type: LibraryContentType) => void;
}

const ALL_CONTENT_TYPES: LibraryContentType[] = [
  "albums",
  "playlists",
  "tracks",
  "artists",
];

export default function Library({
  defaultActive = ["albums", "playlists"],
  exclude = [],
  onItemSelect,
  libraryData,
  loading,
  onRefresh,
}: LibraryProps) {
  const { theme } = useTheme();
  const [selectedItemID, setSelectedItemID] = useState("");
  const [dragKey, setDragKey] = useState<string | null>(null);

  const [active, setActive] = useState<Record<LibraryContentType, boolean>>(() => {
    const base: Record<LibraryContentType, boolean> = {} as any;
    ALL_CONTENT_TYPES.filter((t) => !exclude.includes(t)).forEach((k) => {
      base[k] = defaultActive.includes(k);
    });
    return base;
  });

  const [order, setOrder] = useState<LibraryContentType[]>(
    ALL_CONTENT_TYPES.filter((t) => !exclude.includes(t))
  );

  const toggles = useMemo(
    () =>
      ALL_CONTENT_TYPES.filter((t) => !exclude.includes(t)).map((key) => ({
        key,
        label: key[0].toUpperCase() + key.slice(1),
      })),
    [exclude]
  );

  const handleSelect = (
    item: AlbumType | PlaylistType | TrackType | ArtistType,
    type: LibraryContentType
  ) => {
    setSelectedItemID(item.id);
    onItemSelect?.(item, type);
  };

  const renderItem = (type: LibraryContentType, item: any) => {
    const isSelected = selectedItemID === item.id;
    switch (type) {
      case "playlists":
        return <PlaylistItem playlist={item} isSelected={isSelected} />;
      case "albums":
        return <AlbumItem album={item} isSelected={isSelected} />;
      case "artists":
        return <ArtistItem artist={item} isSelected={isSelected} />;
      case "tracks":
        return <TrackItem track={item} isSelected={isSelected} />;
    }
  };

  const getItems = (type: LibraryContentType) => {
    if (!libraryData) return [];
    return libraryData[type] ?? [];
  };

  const toggleType = (key: LibraryContentType) =>
    setActive((prev) => ({ ...prev, [key]: !prev[key] }));

  const activeKeys = order.filter((k) => active[k]);

  return (
    <div className="library">
      {/* Top buttons */}
      <div className="library-toggles">
        {toggles.map(({ key, label }) => (
          <button
            key={key}
            className={`toggle-btn ${active[key] ? "active" : ""}`}
            onClick={() => toggleType(key)}
          >
            {label}
          </button>
        ))}
      </div>

      {/* Main content grid */}
      <div
        className="library-grid"
        style={{
          gridTemplateColumns: `repeat(${activeKeys.length}, 1fr)`,
        }}
      >
        {activeKeys.map((k) => {
          const items = getItems(k);

          return (
            <div
              key={k}
              className={`library-col ${dragKey === k ? "dragging" : ""}`}
              draggable
              onDragStart={(e) => {
                setDragKey(k);
                e.dataTransfer.setData("text/plain", k);
              }}
              onDragOver={(e) => e.preventDefault()}
              onDrop={(e) => {
                e.preventDefault();
                if (!dragKey || dragKey === k) return;
                const newOrder = [...order];
                const from = newOrder.indexOf(dragKey);
                const to = newOrder.indexOf(k);
                newOrder.splice(from, 1);
                newOrder.splice(to, 0, dragKey);
                setOrder(newOrder);
                setDragKey(null);
              }}
            >
              <div className="col-header">
                <span>{k[0].toUpperCase() + k.slice(1)}</span>
                <RefreshIcon
                  color={theme === "dark" ? "white" : "black"}
                  size={24}
                  loading={loading[k]}
                  onClick={() => onRefresh?.(k)}
                />
              </div>

              <div className="col-body">
                {loading[k] ? (
                  <Loading message={`Loading ${k}...`} />
                ) : items.length > 0 ? (
                  items.map((item: any) => (
                    <div
                      key={item.id}
                      onClick={() => handleSelect(item, k)}
                      className="col-item"
                    >
                      {renderItem(k, item)}
                    </div>
                  ))
                ) : (
                  <div className="empty-msg">No {k} found.</div>
                )}
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
}
