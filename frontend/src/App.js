// frontend/src/App.js

import { useState } from "react";
import Sidebar from "./components/Sidebar";
import Chat     from "./pages/Chat";
import Patients from "./pages/Patients";
import Diagnose from "./pages/Diagnose";
import Vitals   from "./pages/Vitals";
import "./index.css";

const PAGES = { chat: Chat, patients: Patients, diagnose: Diagnose, vitals: Vitals };

export default function App() {
  const [page, setPage] = useState("chat");
  const Page = PAGES[page];

  return (
    <div className="app">
      <Sidebar active={page} onChange={setPage} />
      <main className="main">
        <Page />
      </main>
    </div>
  );
}