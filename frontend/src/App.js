import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';

import Patients from './pages/Patients';
import Events from './pages/Events';
import Resources from './pages/Resources';
import CreateEvent from './pages/CreateEvent';
import Forecast from './pages/Forecast';

import LiveSimulationList from "./pages/LiveSimulationList";
import LiveSimulationDetail from "./pages/LiveSimulationDetail";

import Navbar from './components/Navbar';
import './pages/global.css';

function App() {
  const navbarLinks = [
    { path: '/', label: 'Live Simulation' },   // Home redirects to LIST
    { path: '/patients', label: 'Patients' },
    { path: '/events', label: 'Events' },
    { path: '/resources', label: 'Resources' },
    { path: '/forecast', label: 'Forecast' },
  ];

  return (
    <Router>
      <Navbar title="Hospital AI Dashboard" links={navbarLinks} />

      <div className="container mt-4">
        <Routes>

          {/* ✅ Home = Real-Time Event List */}
          <Route path="/" element={<LiveSimulationList />} />

          {/* ✅ Event Detail Page */}
          <Route path="/live/:eventId" element={<LiveSimulationDetail />} />

          {/* 🔥 REMOVE: LiveSimulation component — no longer used */}

          {/* Other pages */}
          <Route path="/patients" element={<Patients />} />
          <Route path="/events" element={<Events />} />
          <Route path="/resources" element={<Resources />} />
          <Route path="/create-event" element={<CreateEvent />} />
          <Route path="/forecast" element={<Forecast />} />

        </Routes>
      </div>
    </Router>
  );
}

export default App;
