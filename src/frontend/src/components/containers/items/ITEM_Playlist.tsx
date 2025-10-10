import React from "react";
import "./ITEM.css";
import { PlaylistType } from "../../../utils/types/ModelTypes";

export default function PlaylistItem({
  playlist,
  isSelected,
}: {
  playlist: PlaylistType;
  isSelected: boolean;
}) {
  const onDragStart = (e: React.DragEvent<HTMLDivElement>) => {
    e.dataTransfer.effectAllowed = "copyMove";
    try {
      e.dataTransfer.setData(
        "application/json",
        JSON.stringify({
          type: "playlist",
          id: playlist.id,
          name: playlist.name,
        })
      );
    } catch {
      e.dataTransfer.setData("text/plain", playlist.id);
    }
  };

  return (
    <div
      className={`plm-root ${isSelected ? "selected" : ""}`}
      role="button"
      tabIndex={0}
      draggable
      onDragStart={onDragStart}
    >
      <img className="plm-cover" src={playlist.coverURL} alt={playlist.name} />
      <div className="plm-meta">
        <div className="plm-name">{playlist.name}</div>
        <div className="plm-sub">
          {playlist.length ? (
            <span className="plm-length">{playlist.length} songs</span>
          ) : null}
          {playlist.ownerName ? (
            <span className="plm-owner"> • {playlist.ownerName}</span>
          ) : null}
        </div>
      </div>
    </div>
  );
}
