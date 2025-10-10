import React from "react";
import "./Home.css";
import Header from "../components/Header.tsx";
import { title as playlistsTitle, capabilities as playlistsCaps } from "./Playlists";
import { title as libraryTitle, capabilities as libraryCaps } from "./Library";
import { title as userTitle, capabilities as userCaps } from "./User";
import { title as socialTitle, capabilities as socialCaps } from "./Social";
import { title as liveTitle, capabilities as liveCaps } from "./Live";
import { title as gamesTitle, capabilities as gamesCaps } from "./Games";
import { useNavigate } from "react-router-dom";

export default function Home() {
  const navigate = useNavigate();
  const routeMap = {
    [playlistsTitle]: "/playlists",
    [libraryTitle]: "/library",
    [userTitle]: "/user",
    [socialTitle]: "/social",
    [liveTitle]: "/live",
    [gamesTitle]: "/games",
  };

  const handleCardClick = (item) => {
    const path = routeMap[item.title];
    if (path) navigate(path);
  };

  const handleCapabilityClick = (e, item, cap) => {
    e.stopPropagation();
    const path = routeMap[item.title];
    if (path) {
      const params = new URLSearchParams({ cap });
      navigate(`${path}?${params.toString()}`);
    }
  };
  const gridItem = [
    { id: 1, title: playlistsTitle, capabilities: playlistsCaps },
    { id: 2, title: libraryTitle, capabilities: libraryCaps },
    { id: 3, title: userTitle, capabilities: userCaps },
    { id: 4, title: socialTitle, capabilities: socialCaps },
    { id: 5, title: liveTitle, capabilities: liveCaps },
    { id: 6, title: gamesTitle, capabilities: gamesCaps },
  ];


  return (
    <div className="app-container">
      <Header />

      <div className="grid-container">
        {gridItem.map((item) => (
          <div
            key={item.id}
            className="grid-item"
            aria-label={`${item.title} card`}
            role="button"
            tabIndex={0}
            onClick={() => handleCardClick(item)}
            onKeyDown={(e) => {
              if (e.key === "Enter" || e.key === " ") {
                e.preventDefault();
                handleCardClick(item);
              }
            }}
          >
            <div className="grid-item-inner">
              <div className="grid-face grid-face-front">
                {item.title}
              </div>
              <div className="grid-face grid-face-back">
                <div className="grid-back-content">
                  <div className="grid-back-title">{item.title}</div>
                  <ul className="grid-back-list">
                    {item.capabilities?.map((cap, idx) => (
                      <li key={idx}>
                        <button
                          className="grid-back-list-item"
                          onClick={(e) => handleCapabilityClick(e, item, cap)}
                        >
                          {cap}
                        </button>
                      </li>
                    ))}
                  </ul>
                </div>
              </div>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
