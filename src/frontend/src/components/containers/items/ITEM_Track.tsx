import React from "react";
import "./ITEM.css";
import { TrackType } from "../../../utils/types/ModelTypes";

export default function TrackItem({
  track,
  isSelected,
}: {
  track: TrackType;
isSelected: boolean;
}) {


  const onDragStart = (e: React.DragEvent<HTMLDivElement>) => {
    e.dataTransfer.effectAllowed = "copyMove";
    try {
      e.dataTransfer.setData(
        "application/json",
        JSON.stringify({
          type: "track",
          id: track.id,
          name: track.name,
        })
      );
    } catch {
      e.dataTransfer.setData("text/plain", track.id);
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
      {/* Optional album art */}
      {track.album_data?.images?.medium && (
        <img
          className="plm-cover"
          src={track.album_data.images.medium}
          alt={track.name}
        />
      )}
      <div className="plm-meta">
        <div className="plm-name">{track.name}</div>
        <div className="plm-sub">
          {track.artist_data?.length ? (
            <span className="plm-artist">
              {track.artist_data.map((a) => a.name).join(", ")}
            </span>
          ) : null}
          {track.album_data?.name ? (
            <span className="plm-album"> • {track.album_data.name}</span>
          ) : null}
          {track.duration ? (
            <span className="plm-length"> • {Math.floor(track.duration / 60000)}:
              {Math.floor((track.duration % 60000) / 1000)
                .toString()
                .padStart(2, "0")}
            </span>
          ) : null}
        </div>
      </div>
    </div>
  );
}
