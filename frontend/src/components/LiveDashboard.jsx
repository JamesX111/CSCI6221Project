import React from "react";
import useSimulation from "../hooks/useSimulationStream";

export default function LiveDashboard() {
  const events = useSimulation();

  return (
    <div style={{ padding: 20 }}>
      <h2>🚑 Real-Time Emergency Dashboard</h2>

      {events.length === 0 && (
        <p>No incoming events yet… waiting for the simulation...</p>
      )}

      {events.map((ev, index) => (
        <div
          key={index}
          style={{
            marginTop: 15,
            padding: 15,
            border: "1px solid #ddd",
            borderRadius: 8,
            background: "#f9f9f9",
          }}
        >
          <h3>⚠ {ev.event_type.toUpperCase()}</h3>
          <p><strong>Severity:</strong> {ev.severity}</p>
          <p><strong>Location:</strong> {ev.location}</p>
          <p><strong>Predicted Patients:</strong> {ev.predicted}</p>

          <p><strong>Assigned Bed:</strong> {ev.bed_id}</p>

          <p><strong>Patient Info:</strong></p>
          <ul>
            <li>Name: {ev.patient.name}</li>
            <li>Email: {ev.patient.email}</li>
            <li>Phone: {ev.patient.phone}</li>
          </ul>
        </div>
      ))}
    </div>
  );
}
