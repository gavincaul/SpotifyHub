import Home from "./pages/Home.js";
import Playlists from "./pages/Playlists.js";
import Library from "./pages/Library.js";
import User from "./pages/User.js";
import Social from "./pages/Social.js";
import Live from "./pages/Live.js";
import Games from "./pages/Games.js";
import TestAPI from "./pages/TestAPI.js";
import SpotifyCallback from "./pages/SpotifyCallback.js";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import { ThemeProvider } from "./utils/theme/ThemeContext.tsx";
import { DndProvider } from 'react-dnd';
import { HTML5Backend } from 'react-dnd-html5-backend';

function App() {
  return (
    <div>
      <DndProvider backend={HTML5Backend}>
        <ThemeProvider>
          <Router>
            <Routes>
              <Route exact path="/" element={<Home />} />
              <Route exact path="/playlists" element={<Playlists />} />
              <Route exact path="/library" element={<Library />} />
              <Route exact path="/user" element={<User />} />
              <Route exact path="/social" element={<Social />} />
              <Route exact path="/live" element={<Live />} />
              <Route exact path="/games" element={<Games />} />
              <Route exact path="/testAPI" element={<TestAPI />} />
              <Route path="/spotify/callback" element={<SpotifyCallback />} />
              <Route exact path="*" element={<Home />} />
            </Routes>
          </Router>
        </ThemeProvider>
      </DndProvider>
    </div>
  );
}

export default App;
