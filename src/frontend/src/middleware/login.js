import { useApi } from "./apiClient.js";

export const useSpotifyLogin = () => {
  const { get } = useApi();

  const loginWithSpotify = async () => {
    try {
      // Save current page so we can return here after login
      localStorage.setItem("preLoginURL", window.location.href);

      console.log("Login with Spotify initiated");
      // Step 1: Get auth URL from backend
      const data = await get("/me/login/start");
      if (!data.auth_url) throw new Error("No auth URL returned from backend");

      // Step 2: Redirect user to Spotify OAuth page
      window.location.href = data.auth_url;
    } catch (err) {
      console.error("Login failed:", err);
      alert("Login failed: " + err.message);
    }
  };

  const handlePostLogin = async () => {
    const params = new URLSearchParams(window.location.search);
    const userId = params.get("user_id");
    if (userId) {
      // Store user ID in session
      sessionStorage.setItem("userId", userId);
      const user_data = await get("/me/get");
      sessionStorage.setItem("userData", JSON.stringify(user_data));
      // Return user to page they were on
      const preLoginURL = localStorage.getItem("preLoginURL");
      if (preLoginURL) {
        localStorage.removeItem("preLoginURL");
        window.location.href = preLoginURL;
      } else {
        window.location.href = "/"; // fallback
      }
    }
  };

  return { loginWithSpotify, handlePostLogin };
};

export const useSpotifyLogout = () => {
  const { post } = useApi();

  // Only clears Spotify session and sessionStorage
  const logoutFromSpotify = async () => {
    try {
      console.log("Logging out from Spotify...");
      await post("/me/logout"); // can check response if needed

      // Clear frontend session
      sessionStorage.removeItem("userId");
      sessionStorage.removeItem("userData");

      console.log("Frontend session cleared.");
    } catch (err) {
      console.error("Logout failed:", err);
      alert("Logout failed: " + err.message);
    }
  };

  // Separate post-logout behavior, e.g., redirect
  const handlePostLogout = (redirectURL = "/") => {
    const preLoginURL = localStorage.getItem("preLoginURL");
    if (preLoginURL) {
      localStorage.removeItem("preLoginURL");
      window.location.href = preLoginURL;
    } else {
      window.location.href = redirectURL;
    }
  };

  return { logoutFromSpotify, handlePostLogout };
};
