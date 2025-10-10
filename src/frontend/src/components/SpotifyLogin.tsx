import React, { useState } from "react";
import { useSpotifyLogin, useSpotifyLogout } from "../middleware/login.js";

const SpotifyLogin = () => {
  const { loginWithSpotify } = useSpotifyLogin();
  const { logoutFromSpotify, handlePostLogout } = useSpotifyLogout();

  const [loading, setLoading] = useState(false);
  const [message, setMessage] = useState("");
  // eslint-disable-next-line
  const [loggedIn, setLoggedIn] = useState(
    sessionStorage.getItem("userId") !== null
  );
  const handleLogin = async () => {
    setLoading(true);
    setMessage("");

    try {
      await loginWithSpotify();
      setMessage("Redirecting to Spotify...");
    } catch (err) {
      console.error("Login failed:", err);
      setMessage("Login failed: " + err.message);
    } finally {
      setLoading(false);
    }
  };
  const handleLogout = async () => {
    setLoading(true);
    setMessage("");

    try {
      await logoutFromSpotify();
      setMessage("Redirecting to Spotify...");
    } catch (err) {
      console.error("Logout failed:", err);
      setMessage("Logout failed: " + err.message);
    } finally {
      handlePostLogout(); 
      setLoading(false);
    }
  };

  return (
    <>
      {loggedIn ? (
        <div style={{ padding: "20px", fontFamily: "Arial" }}>
          <button onClick={handleLogout} disabled={loading}>
            {loading ? "Loading..." : "Logout from Spotify"}
          </button>
          {message && <p style={{ marginTop: "10px" }}>{message}</p>}
        </div>
      ) : (
        <div style={{ padding: "20px", fontFamily: "Arial" }}>
          <button onClick={handleLogin} disabled={loading}>
            {loading ? "Loading..." : "Login with Spotify"}
          </button>
          {message && <p style={{ marginTop: "10px" }}>{message}</p>}
        </div>
      )}
    </>
  );
};

export default SpotifyLogin;
