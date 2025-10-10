import React from "react";
import "./Header.css";
import { useTheme } from "../utils/theme/ThemeContext.tsx";
import SunIcon from "./ui/icons/SunIcon.tsx";
import MoonIcon from "./ui/icons/MoonIcon.tsx";
import ProfileIcon from "./ui/icons/PFPIcon.tsx";
import LibraryIcon from "./ui/icons/LibraryIcon.tsx";
import { useNavigate } from "react-router-dom";

type HeaderProps = {
  includeLibraryButton?: boolean;
};

export default function Header({ includeLibraryButton = false }: HeaderProps) {
  const { theme, toggleTheme } = useTheme();
  const navigate = useNavigate();

  return (
    <div className="header">
      <div className="left-controls">
        <button onClick={toggleTheme} className="btn" title="Toggle Theme">
          {theme === "dark" ? (
            <SunIcon color="white" size={32} />
          ) : (
            <MoonIcon color="black" size={32} />
          )}
        </button>

        {includeLibraryButton && (
          <button
            onClick={() => navigate("/library")}
            className="btn"
            title="Library"
          >
            <LibraryIcon
              color={theme === "dark" ? "white" : "black"}
              size={32}
            />
          </button>
        )}
      </div>

      <h1 className="title" onClick={() => navigate("/")}>
        SPOTIFYHUB
      </h1>

      <div className="profile-icon" title="Profile">
        <ProfileIcon
          fill="black"
          color={theme === "dark" ? "white" : "black"}
        />
      </div>
    </div>
  );
}
