import React, { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import "./LiveSimulationList.css";

export default function LiveSimulationList() {
  const [events, setEvents] = useState([]);
  const navigate = useNavigate();

  useEffect(() => {
    const fetchEvents = async () => {
      try {
        const res = await fetch("http://localhost:5000/api/live-events");
        const data = await res.json();
        setEvents(data);
      } catch (err) {
        console.error("Failed to load live events:", err);
      }
    };

    fetchEvents();
    const interval = setInterval(fetchEvents, 3000);
    return () => clearInterval(interval);
  }, []);

  // Convert severity (1-5) into HSL color (green → red)
  const getSeverityColor = (severity) => {
    const sev = Math.min(Math.max(severity, 1), 5); // clamp between 1 and 5
    const hue = 120 - ((sev - 1) * 120) / 4; // 1 → green, 5 → red
    return `hsl(${hue}, 80%, 85%)`;
  };

  return (
    <div className="container">
      <h2>Active Live Events</h2>

      {events.length === 0 ? (
        <p>No active hospital events…</p>
      ) : (
        <table className="events-table">
          <thead>
            <tr>
              <th>Event Type</th>
              <th>Severity</th>
              <th>Location</th>
            </tr>
          </thead>
          <tbody>
            {events.map((evt) => {
              const base = evt.raw_event || evt.event || evt;
              return (
                <tr
                  key={evt.event_id}
                  className="clickable-row"
                  style={{ backgroundColor: getSeverityColor(base.severity) }}
                  onClick={() => navigate(`/live/${evt.event_id}`)}
                >
                  <td>{base.event_type}</td>
                  <td>{base.severity}</td>
                  <td>{base.location}</td>
                </tr>
              );
            })}
          </tbody>
        </table>
      )}
    </div>
  );
}
