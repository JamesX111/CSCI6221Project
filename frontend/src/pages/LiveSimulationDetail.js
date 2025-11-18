// src/pages/LiveSimulationDetail.js
import React, { useEffect, useState } from "react";
import { useParams } from "react-router-dom";

export default function LiveSimulationDetail() {
  const { eventId } = useParams();
  const [eventData, setEventData] = useState(null);
  const [accepting, setAccepting] = useState(false);
  const [acceptError, setAcceptError] = useState("");

  const fetchEvent = async () => {
    try {
      const res = await fetch("http://localhost:5000/api/live-events");
      const all = await res.json();
      const selected = all.find((e) => e.event_id === eventId);
      setEventData(selected || null);
    } catch (err) {
      console.error("Error loading event detail:", err);
    }
  };

  useEffect(() => {
    fetchEvent();
    const interval = setInterval(fetchEvent, 2000);
    return () => clearInterval(interval);
  }, [eventId]);

  if (!eventData) return <p>Loading event…</p>;

  const raw = eventData.raw_event || eventData.event || eventData;
  const { event_type, severity, location } = raw;
  const { predicted, allocations, summary } = eventData;
  const accepted = !!eventData.accepted;

  // -----------------------------------------------------------
  // ⭐ FIXED: Accept event & store staff names
  // -----------------------------------------------------------
  const handleAccept = async () => {
    setAccepting(true);
    setAcceptError("");

    try {
      const payload = {
        event_id: eventData.event_id,
        patients: predicted,
        severity,
        event_type,
        location,
      };

      const res = await fetch("http://localhost:5000/api/accept_event", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload),
      });

      if (!res.ok) {
        const errData = await res.json().catch(() => ({}));
        throw new Error(errData.error || "Failed to accept event");
      }

      const data = await res.json();

      // ⭐ FIX: Store staff object including names
      setEventData((prev) => ({
        ...prev,
        accepted: true,
        accepted_beds: data.assigned_beds || [],
        assigned_staff: data.assigned_staff || null
      }));
    } catch (err) {
      console.error(err);
      setAcceptError(err.message || "Error accepting event");
    } finally {
      setAccepting(false);
    }
  };

  const displayAllocations = () => {
    if (eventData.accepted && eventData.accepted_beds) {
      return eventData.accepted_beds.map((bedId, idx) => ({
        patient_id: idx + 1,
        bed_id: bedId,
      }));
    }
    return allocations || [];
  };

  const shownAllocations = displayAllocations();

  // ⭐ Use names if available
  const assignedStaff = eventData.assigned_staff || {};

  const nurseName = assignedStaff.nurse || "N/A";
  const helperName = assignedStaff.helper || "N/A";

  return (
    <div className="live-container">
      <h2>Real-Time Hospital Simulation</h2>

      <div className="card">
        <h3>🚨 Event Detected</h3>
        <p><strong>Type:</strong> {event_type}</p>
        <p><strong>Severity:</strong> {severity}</p>
        <p><strong>Location:</strong> {location}</p>
        <p><strong>Incoming Patients:</strong> {predicted}</p>

        <p>
          <strong>Status:</strong>{" "}
          {accepted ? "Accepted and resources booked" : "Pending (simulation only)"}
        </p>

        {!accepted && (
          <button onClick={handleAccept} disabled={accepting} style={{ marginTop: "10px" }}>
            {accepting ? "Accepting..." : "Accept Event & Allocate Resources"}
          </button>
        )}

        {acceptError && (
          <p style={{ color: "red", marginTop: "8px" }}>Error: {acceptError}</p>
        )}
      </div>

      {/* ----------------------------------------------------
           ⭐ NEW: SHOW STAFF NAMES (no ID flashing)
         ---------------------------------------------------- */}
      {accepted && assignedStaff && (
        <div className="card">
          <h3>👩‍⚕️ Assigned Staff</h3>

          <p>
            <strong>Nurse:</strong> {nurseName ? nurseName : "N/A"}
          </p>

          <p>
            <strong>Helper:</strong> {helperName ? helperName : "N/A"}
          </p>
        </div>
      )}

      <div className="card">
        <h3>🛏 Bed Assignments</h3>

        {!accepted ? (
          <p>Pending — beds will be assigned once the event is accepted.</p>
        ) : (
          shownAllocations.length > 0 ? (
            shownAllocations.map((a, i) => (
              <p key={i}>
                Patient #{a.patient_id} → Assigned to Bed {a.bed_id}
              </p>
            ))
          ) : (
            <p>No assigned beds.</p>
          )
        )}
      </div>


      <div className="card">
        <h3>🤖 AI Summary</h3>
        <p>{summary}</p>
      </div>
    </div>
  );
}
