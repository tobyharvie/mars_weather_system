import { useState } from 'react'
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import Navbar from "./components/Navbar";
import Home from "./pages/home";
import About from "./pages/About";
import './style/App.css'

function App() {
  return (
    <div className="h-screen w-screen bg-cover bg-center bg-no-repeat bg-[url('elysium.jpg')]">
      <Router>
        <Navbar />
        <main className="pt-16 px-4">  {/* Add padding-top if navbar is fixed */}
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/about" element={<About />} />
        </Routes>
        </main>
      </Router>
    </div>
  );
}

export default App;
