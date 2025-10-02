import React from "react";
import { useLocation } from "react-router-dom";

export const title = "Social";
export const capabilities = ["Friends", "Share"];

export default function Social() {
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
      <p>Tools and settings for social features will appear here.</p>
    </div>
  );
}

