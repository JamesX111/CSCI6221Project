import React, { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import "./LiveSimulationList.css";

export default function LiveSimulationList() {
  const [events, setEvents] = useState([]);
  const [severityFilter, setSeverityFilter] = useState("all");
  const [statusFilter, setStatusFilter] = useState("all"); // all | accepted | pending
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

  const filteredEvents = events.filter((evt) => {
    const base = evt.raw_event || evt.event || evt;
    const sevMatches =
      severityFilter === "all" ||
      String(base.severity) === String(severityFilter);

    const accepted = !!evt.accepted;
    const statusMatches =
      statusFilter === "all" ||
      (statusFilter === "accepted" && accepted) ||
      (statusFilter === "pending" && !accepted);

    return sevMatches && statusMatches;
  });

  return (
    <div className="container">
      <h2>Active Live Events</h2>

      {/* Filters Row */}
      <div
        className="filters-row"
        style={{
          display: "flex",
          gap: "20px",
          alignItems: "center",
          marginBottom: "15px",
        }}
      >
        {/* 🔽 Severity Filter */}
        <div className="severity-filter">
          <label style={{ marginRight: "10px", fontWeight: "bold" }}>
            Filter by Severity:
          </label>
          <select
            value={severityFilter}
            onChange={(e) => setSeverityFilter(e.target.value)}
            className="severity-dropdown"
          >
            <option value="all">All</option>
            <option value="1">1 (Low)</option>
            <option value="2">2</option>
            <option value="3">3 (Medium)</option>
            <option value="4">4</option>
            <option value="5">5 (High)</option>
          </select>
        </div>

        {/* 🔽 Acceptance Filter */}
        <div className="status-filter">
          <label style={{ marginRight: "10px", fontWeight: "bold" }}>
            Status:
          </label>
          <select
            value={statusFilter}
            onChange={(e) => setStatusFilter(e.target.value)}
          >
            <option value="all">All</option>
            <option value="accepted">Accepted</option>
            <option value="pending">Not Accepted</option>
          </select>
        </div>
      </div>

      {filteredEvents.length === 0 ? (
        <p>No events match this filter.</p>
      ) : (
        <table className="events-table">
          <thead>
            <tr>
              <th>Event Type</th>
              <th>Severity</th>
              <th>Location</th>
              <th>Status</th>
            </tr>
          </thead>
          <tbody>
            {filteredEvents.map((evt) => {
              const base = evt.raw_event || evt.event || evt;
              const accepted = !!evt.accepted;
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
                  <td>{accepted ? "Accepted" : "Pending"}</td>
                </tr>
              );
            })}
          </tbody>
        </table>
      )}
    </div>
  );
}
