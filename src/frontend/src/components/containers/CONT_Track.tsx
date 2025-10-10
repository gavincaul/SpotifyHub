import React from "react";
import "./CONT_Track.css";
import { TrackType } from "../../utils/types/ModelTypes.ts";

export default function TrackContainer({ track }: { track: TrackType }) {
  if (!track) return <div className="track-error">No track data.</div>;

  const artists = track.artist_data?.map((a) => a.name).join(", ") || "Unknown";
  const albumCover =
    track.album_data?.images?.large ||
    track.album_data?.images?.medium ||
    track.album_data?.images?.small ||
    "";
  console.log(track.duration_ms);
  return (
    <div className="track-model">
      <div className="track-top">
        {/* Left: Album Cover */}
        <div className="track-cover-wrap">
          <img
            src={albumCover}
            alt={`${track.album_data?.name || "Unknown Album"} cover`}
            className="track-cover"
          />
        </div>

        {/* Right: Metadata */}
        <div className="track-meta">
          <div className="track-meta-inner">
            <div className="track-artist">{artists}</div>
            <h2 className="track-title">{track.name}</h2>
            <div className="track-album">{track.album_data?.name}</div>

            <div className="track-info">
              <span>
                {Math.floor(track.duration_ms / 60000)}:
                {String(
                  Math.floor((track.duration_ms % 60000) / 1000)
                ).padStart(2, "0")}
              </span>
              {track.explicit && <span className="explicit-badge">E</span>}
              {track.popularity && (
                <span className="track-popularity">
                  Popularity: {track.popularity}
                </span>
              )}
            </div>

            {track.url && (
              <a
                href={track.url}
                target="_blank"
                rel="noreferrer"
                className="track-link"
              >
                Open in Spotify
              </a>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}
