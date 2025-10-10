
import React from "react";
import "./ITEM.css";
import { ArtistType } from "../../../utils/types/ModelTypes";

export default function ArtistItem({
  artist,
  isSelected,
}: {
  artist: ArtistType;
  isSelected: boolean;
}) {


  const onDragStart = (e: React.DragEvent<HTMLDivElement>) => {
    e.dataTransfer.effectAllowed = "copyMove";
    try {
      e.dataTransfer.setData(
        "application/json",
        JSON.stringify({
          type: "artist",
          id: artist.id,
          name: artist.name,
        })
      );
    } catch {
      e.dataTransfer.setData("text/plain", artist.id);
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
      {/* Optional artist image */}
      {artist.images.large && (
        <img
          className="plm-cover"
          src={artist.images.large}
          alt={artist.name}
        />
      )}
      <div className="plm-meta">
        <div className="plm-name">{artist.name}</div>
        <div className="plm-sub">
          {artist.followers ? (
            <span className="plm-followers">{artist.followers.toLocaleString()} followers</span>
          ) : null}
          {artist.genres?.length ? (
            <span className="plm-genres"> • {artist.genres.join(", ")}</span>
          ) : null}
        </div>
      </div>
    </div>
  );
}
