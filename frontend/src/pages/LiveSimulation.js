// src/pages/LiveSimulation.js
import React from "react";
import useSimulationStream from "../hooks/useSimulationStream";
import "./LiveSimulation.css";

export default function LiveSimulation() {
  const data = useSimulationStream();

  if (!data) {
    return (
      <div className="live-container">
        <h2>Real-Time Simulation</h2>
        <p>Waiting for live hospital events…</p>
      </div>
    );
  }

  const {
    event_type,
    severity,
    location,
    predicted,
    allocations,
    summary
  } = data;

  return (
    <div className="live-container">
      <h2 className="title">Real-Time Hospital Simulation</h2>

      {/* Event Card */}
      <div className="card event-card">
        <h3> Event Detected</h3>
        <p><strong>Type:</strong> {event_type}</p>
        <p><strong>Severity:</strong> {severity}</p>
        <p><strong>Location:</strong> {location}</p>
        <p><strong>Incoming Patients:</strong> {predicted}</p>
      </div>

      {/* Bed Allocation */}
      <div className="card beds-card">
        <h3>Bed Assignments</h3>

        {allocations.length === 0 && <p>No patients this cycle.</p>}

        {allocations.map((entry, index) => (
          <div key={index} className="bed-row">
            <span>Patient #{entry.patient_id}</span>
            {entry.bed_id ? (
              <span className="assigned">Assigned to Bed {entry.bed_id}</span>
            ) : (
              <span className="waiting">Waiting</span>
            )}
          </div>
        ))}
      </div>

      {/* AI Summary */}
      <div className="card ai-card">
        <h3>AI Summary</h3>
        <p>{summary}</p>
      </div>
    </div>
  );
}
