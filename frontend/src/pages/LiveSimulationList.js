// src/pages/LiveSimulation.js  (your "list" page)
import React, { useEffect, useState } from "react";
import { Link } from "react-router-dom";

export default function LiveSimulationList() {
  const [events, setEvents] = useState([]);

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

  return (
    <div className="container">
      <h2>Active Live Events</h2>

      {events.length === 0 && <p>No active hospital events…</p>}

      {events.map(evt => {
        // 👇 support both old (raw_event) and future flattened shapes
        const base = evt.raw_event || evt.event || evt;

        return (
          <div key={evt.event_id} className="event-card">
            <h3>{base.event_type}</h3>
            <p><strong>Severity:</strong> {base.severity}</p>
            <p><strong>Location:</strong> {base.location}</p>

            <Link to={`/live/${evt.event_id}`} className="btn btn-primary">
              View Event
            </Link>
          </div>
        );
      })}
    </div>
  );
}
