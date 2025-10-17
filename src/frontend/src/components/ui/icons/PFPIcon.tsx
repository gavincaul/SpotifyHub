import React, { useState, useEffect } from "react";
import SpotifyLogin from "../../SpotifyLogin.tsx";

interface IconProps {
  size?: number;
  color?: string;
  fill?: string;
}

export default function PFPIcon({
  size = 32,
  color = "currentColor",
  fill = "none",
}: IconProps) {
  // State derived from sessionStorage
  const [userData, setUserData] = useState(() => {
    const data = sessionStorage.getItem("userData");
    return data ? JSON.parse(data) : null;
  });

  const [showLogin, setShowLogin] = useState(false);

  const loggedIn = !!userData;
  const userName = userData?.display_name || "Guest";
  const userId = userData?.user_id || "N/A";
  const userImg = userData?.images?.large || null;

  // Function to clear sessionStorage and reset state
  const clearSession = () => {

    sessionStorage.removeItem("userId");
    sessionStorage.removeItem("userData");
    setUserData(null);
  };

  // Global listener for auth errors
  useEffect(() => {
    const handleAuthError = (e: CustomEvent) => {
      if (e.detail?.isAuthError) {
        console.warn("Auth error detected, clearing session...");
        clearSession();
      }
    };

    window.addEventListener("spotifyAuthError", handleAuthError as EventListener);

    return () => {
      window.removeEventListener("spotifyAuthError", handleAuthError as EventListener);
    };
  }, []);

  const handleClick = () => setShowLogin((prev) => !prev);

  return (
    <div
      style={{ position: "relative", display: "inline-block", cursor: "pointer" }}
      onClick={handleClick}
      title="User Profile"
    >
      {loggedIn ? (
        userImg ? (
          <img
            src={userImg}
            alt="User"
            width={50}
            height={50}
            style={{ borderRadius: "50%", objectFit: "cover", display: "block" }}
          />
        ) : (
          <span>User</span>
        )
      ) : (
        <svg width={size} height={size} viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
          <path
            d="M19.7274 20.4471C19.2716 19.1713 18.2672 18.0439 16.8701 17.2399C15.4729 16.4358 13.7611 16 12 16C10.2389 16 8.52706 16.4358 7.12991 17.2399C5.73276 18.0439 4.72839 19.1713 4.27259 20.4471"
            stroke={color}
            strokeWidth="1.2"
            strokeLinecap="round"
          />
          <circle
            cx="12"
            cy="8"
            r="4"
            fill={fill}
            stroke={color}
            strokeWidth="1.2"
            strokeLinecap="round"
          />
        </svg>
      )}

      {showLogin && (
        <div
          style={{
            position: "absolute",
            top: 50 + 8,
            right: 0,
            cursor: "default",
            minWidth: "220px",
            backgroundColor: "#fff",
            border: "1px solid #ccc",
            borderRadius: "8px",
            boxShadow: "0 4px 8px rgba(0,0,0,0.1)",
            padding: "12px",
            zIndex: 100,
          }}
        >
          <SpotifyLogin />
          {loggedIn && (
            <div style={{ marginTop: "12px" }}>
              <strong>User Info</strong>
              <p style={{ margin: "4px 0" }}>Name: {userName}</p>
              <p style={{ margin: "4px 0" }}>ID: {userId}</p>
            </div>
          )}
        </div>
      )}
    </div>
  );
}
