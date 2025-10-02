import React from "react";
import { useLocation } from "react-router-dom";
import Header from "../components/Header.tsx";
import LibraryComponent from "../components/Library.tsx";

export const title = "Your Library";
export const capabilities = ["Liked Songs", "Albums", "Artists"];

export default function Library() {
  const { search } = useLocation();
  const params = new URLSearchParams(search);
  const activated = params.get("cap");
  return (
    <div className="app-container">
      <Header includeLibraryButton />
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
      <LibraryComponent />
      </div>
    </div>
  );
}

