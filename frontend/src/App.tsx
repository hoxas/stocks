import { useState } from "react";
import reactLogo from "./assets/react.svg";
import "./App.css";
import Dashboard from "./components/Dashboard";

function App() {
  return (
    <div className="App min-h-screen min-w-full flex items-center justify-center">
      <Dashboard />
    </div>
  );
}

export default App;
