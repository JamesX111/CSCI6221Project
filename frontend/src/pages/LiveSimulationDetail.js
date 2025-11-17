// src/pages/LiveSimulationDetail.js
import React, { useEffect, useState } from "react";
import { useParams } from "react-router-dom";

export default function LiveSimulationDetail() {
  const { eventId } = useParams();
  const [eventData, setEventData] = useState(null);

  useEffect(() => {
    const fetchEvent = async () => {
      try {
        const res = await fetch("http://localhost:5000/api/live-events");
        const all = await res.json();
        const selected = all.find(e => e.event_id === eventId);
        setEventData(selected || null);
      } catch (err) {
        console.error("Error loading event detail:", err);
      }
    };

    fetchEvent();
    const interval = setInterval(fetchEvent, 2000);
    return () => clearInterval(interval);
  }, [eventId]);

  if (!eventData) return <p>Loading event…</p>;

  // 👇 pull the actual event fields from raw_event / event / top-level
  const raw = eventData.raw_event || eventData.event || eventData;
  const { event_type, severity, location } = raw;
  const { predicted, allocations, summary } = eventData;

  return (
    <div className="live-container">
      <h2>Real-Time Hospital Simulation</h2>

      <div className="card">
        <h3>🚨 Event Detected</h3>
        <p><strong>Type:</strong> {event_type}</p>
        <p><strong>Severity:</strong> {severity}</p>
        <p><strong>Location:</strong> {location}</p>
        <p><strong>Incoming Patients:</strong> {predicted}</p>
      </div>

      <div className="card">
        <h3>🛏 Bed Assignments</h3>
        {allocations && allocations.length > 0 ? (
          allocations.map((a, i) => (
            <p key={i}>
              Patient #{a.patient_id} →{" "}
              {a.bed_id ? `Assigned to Bed ${a.bed_id}` : "Waiting"}
            </p>
          ))
        ) : (
          <p>No patients this cycle.</p>
        )}
      </div>

      <div className="card">
        <h3>🤖 AI Summary</h3>
        <p>{summary}</p>
      </div>
    </div>
  );
}
