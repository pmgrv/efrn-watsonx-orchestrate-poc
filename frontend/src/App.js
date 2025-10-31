import React from "react";
import Dashboard from "./components/Dashboard";

function App() {
  return (
    <div style={{ padding: "2rem", fontFamily: "Arial" }}>
      <h1 style={{ textAlign: "center", color: "#0043ce" }}>
        EFRN – AI Orchestrated Financial Trust Network
      </h1>
      <Dashboard />
    </div>
  );
}

export default App;