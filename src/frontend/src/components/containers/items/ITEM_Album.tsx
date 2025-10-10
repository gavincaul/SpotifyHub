
import React from "react";
import "./ITEM.css";
import { AlbumType } from "../../../utils/types/ModelTypes";

export default function AlbumItem({
  album,
  isSelected
}: {
  album: AlbumType;
  isSelected: boolean;
}) {

  const onDragStart = (e: React.DragEvent<HTMLDivElement>) => {
    e.dataTransfer.effectAllowed = "copyMove";
    try {
      e.dataTransfer.setData(
        "application/json",
        JSON.stringify({
          type: "playlist",
          id: album.id,
          name: album.name,
        })
      );
    } catch {
      e.dataTransfer.setData("text/plain", album.id);
    }
  };
  console.log(album)
  return (
    <div
      className={`plm-root ${isSelected ? "selected" : ""}`}
      role="button"
      tabIndex={0}
      draggable
      onDragStart={onDragStart}
    >
      <img className="plm-cover" src={album.images?.large || ""} alt={album.name} />
      <div className="plm-meta">
        <div className="plm-name">{album.name}</div>
        <div className="plm-sub">
          {album.total_tracks ? (
            <span className="plm-length">{album.total_tracks} songs</span>
          ) : null}
          {album.artists ? (
            <span className="plm-owner"> • {album.artists.map((a)=> a.name)}</span>
          ) : null}
        {album.release_date ? (
            <span className="plm-length"> • {album.release_date}</span>
          ) : null}
        </div>
      </div>
    </div>
  );
}
