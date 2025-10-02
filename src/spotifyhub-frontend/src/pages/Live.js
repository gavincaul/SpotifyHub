import React from "react";
import { useLocation } from "react-router-dom";

export const title = "Live";
export const capabilities = ["Now Playing", "Queue"];

export default function Live() {
  const { search } = useLocation();
  const params = new URLSearchParams(search);
  const activated = params.get("cap");
  return (
    <div style={{ padding: 16 }}>
      {activated && (
        <div style={{
          marginBottom: 12,
          padding: 10,
          borderRadius: 8,
          background: "rgba(29,185,84,0.15)",
          color: "var(--text)",
          border: "1px solid rgba(29,185,84,0.35)",
          fontWeight: 600,
        }}>
          Activated capability: {activated}
        </div>
      )}
      <h1>{title}</h1>
      <p>Live playback information and queue management will be available here.</p>
    </div>
  );
}

