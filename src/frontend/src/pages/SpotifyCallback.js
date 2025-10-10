import { useEffect } from "react";
import Loading from "../components/ui/elements/Loading.tsx";
import { useApi } from "../middleware/apiClient";

const SpotifyCallback = () => {
  const { get } = useApi();
  useEffect(() => {
    const params = new URLSearchParams(window.location.search);
    const code = params.get("code");

    if (!code) {
      alert("Spotify login failed: missing code");
      return;
    }
    get(`/me/login/callback?code=${code}`)
      .then((data) => {
        // Step 2: Save user ID
        if (data.user_id) sessionStorage.setItem("userId", data.user_id);
        if (data.user_data)
          sessionStorage.setItem("userData", JSON.stringify(data.user_data));
        // Step 3: Redirect back to page before login
        const redirectUrl = localStorage.getItem("preLoginURL") || "/";
        console.log("Redirecting to:", redirectUrl);
        localStorage.removeItem("preLoginURL");
        window.location.href = redirectUrl;
      })
      .catch((err) => {
        console.error("Login finish failed:", err);
        alert("Login failed. Check console.");
      });
  }, [get]);

  return (
    <div
      className="app-container"
      style={{
        display: "flex",
        justifyContent: "center",
        alignItems: "center",
        margin: "auto",
      }}
    >
      <Loading message="Processing Spotify Login..." />
    </div>
  );
};

export default SpotifyCallback;
