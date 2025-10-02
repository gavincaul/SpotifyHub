import React from "react";
import "./PlaylistModel.css";

export type PlaylistModelProps = {
  id: string;
  imageUrl: string;
  name: string;
  length?: string; // e.g., "42 songs" or duration
  owner?: string;  // e.g., "You" or display name
  onOpen?: (id: string) => void; // open on page
};

export default function PlaylistModel({ id, imageUrl, name, length, owner, onOpen }: PlaylistModelProps) {
  const onClick = () => {
    onOpen?.(id);
  };

  const onDragStart = (e: React.DragEvent<HTMLDivElement>) => {
    e.dataTransfer.effectAllowed = "copyMove";
    try {
      e.dataTransfer.setData("application/json", JSON.stringify({ type: "playlist", id, name }));
    } catch {
      e.dataTransfer.setData("text/plain", id);
    }
  };

  return (
    <div
      className="plm-root"
      role="button"
      tabIndex={0}
      onClick={onClick}
      onKeyDown={(e) => { if (e.key === "Enter") onClick(); }}
      draggable
      onDragStart={onDragStart}
    >
      <img className="plm-cover" src={imageUrl} alt={name} />
      <div className="plm-meta">
        <div className="plm-name">{name}</div>
        <div className="plm-sub">
          {length ? <span className="plm-length">{length}</span> : null}
          {owner ? <span className="plm-owner"> • {owner}</span> : null}
        </div>
      </div>
    </div>
  );
}

