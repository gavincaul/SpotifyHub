import React from "react";
import "./TrackModel.css";

export type TrackModelProps = {
  id: string;
  albumArt: string;
  title: string;
  artist: string;
  album: string;
  duration: number | string;
  playCount?: number;
  releaseDate?: string;
  isSelected?: boolean;
  onClick?: (id: string) => void;
  // index intentionally NOT required here — parent renders the idx cell
};

const formatDuration = (ms: number): string => {
  if (typeof ms !== "number") return String(ms);
  const minutes = Math.floor(ms / 60000);
  const seconds = Math.floor((ms % 60000) / 1000)
    .toString()
    .padStart(2, "0");
  return `${minutes}:${seconds}`;
};

const formatNumber = (num?: number): string => {
  if (num === undefined) return "";
  return num.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",");
};

const TrackModel: React.FC<TrackModelProps> = ({
  id,
  albumArt,
  title,
  artist,
  album,
  duration,
  playCount,
  releaseDate,
  isSelected = false,
  onClick,
}) => {
  const handleClick = () => {
    if (onClick) onClick(id);
  };

  return (
    <>
      {/* Title column (album art + title + artist) */}
      <div className="td td-title">
        <div
          className={`track-model ${isSelected ? "selected" : ""}`}
          onClick={handleClick}
          role="row"
          aria-selected={isSelected}
        >
          <div className="track-album-art">
            <img src={albumArt} alt={`${title} album art`} />
          </div>
          <div className="track-info">
            <div className="track-title">{title}</div>
            <div className="track-artist">{artist}</div>
          </div>
        </div>
      </div>

      {/* Other columns — these are direct grid cells */}
      <div className="td td-album">{album}</div>

      <div className="td td-time">
        {typeof duration === "number" ? formatDuration(duration) : duration}
      </div>

      <div className="td td-playcount">{playCount !== undefined ? formatNumber(playCount) : ""}</div>

      <div className="td td-release-date">{releaseDate ? new Date(releaseDate).getFullYear() : ""}</div>
    </>
  );
};

export default TrackModel;
