import React from "react";
import { Routes, Route } from "react-router-dom";
import { LandingPage } from "./pages/LandingPage/LandingPage";
import { ChatPage } from "./pages/ChatPage";
import "./styles/global.css";

function App(): React.ReactNode {
  return (
    <Routes>
      <Route path="/" element={<LandingPage />} />
      <Route path="/agent" element={<ChatPage />} />
    </Routes>
  );
}

export default App;
