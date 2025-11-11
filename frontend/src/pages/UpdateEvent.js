import React, { useState, useEffect } from "react";
import { useNavigate, useParams } from "react-router-dom";

const UpdateEvent = () => {
  const { eventId } = useParams();
  const navigate = useNavigate();
  const [eventData, setEventData] = useState({
    event_type: "",
    description: "",
    patient_id: "",
    doctor_id: "",
    scheduled_at: "",
    status: "Scheduled",
    payment_amount: "",
    payment_method: "",
  });
  const [error, setError] = useState("");

  useEffect(() => {
    const fetchEvent = async () => {
      try {
        const res = await fetch(
          `http://127.0.0.1:5000/api/events/get_event/${eventId}`,
          { method: "POST" }
        );
        const data = await res.json();
        if (!res.ok) {
          setError(data.error || "Failed to load event");
        } else {
          setEventData({
            event_type: data.event_type || "",
            description: data.description || "",
            patient_id: data.patient ? data.patient.id : "",
            doctor_id: data.doctor ? data.doctor.id : "",
            scheduled_at: data.scheduled_at
              ? data.scheduled_at.replace(" ", "T")
              : "",
            status: data.status || "Scheduled",
            payment_amount: data.payment?.amount || "",
            payment_method: data.payment?.method || "",
          });
        }
      } catch (err) {
        setError("Failed to load event");
        console.error(err);
      }
    };
    fetchEvent();
  }, [eventId]);

  const handleChange = (e) => {
    setEventData({ ...eventData, [e.target.name]: e.target.value });
  };

  const handleUpdate = async () => {
    setError("");
    try {
      const res = await fetch(
        `http://127.0.0.1:5000/api/events/update_event/${eventId}`,
        {
          method: "PUT",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify(eventData),
        }
      );
      const data = await res.json();
      if (!res.ok) {
        setError(data.error || "Update failed");
      } else {
        navigate("/events");
      }
    } catch (err) {
      setError("Failed to update event");
      console.error(err);
    }
  };

  const handleDelete = async () => {
    if (!window.confirm("Are you sure you want to delete this event?")) return;
    try {
      const res = await fetch(
        `http://127.0.0.1:5000/api/events/delete_event/${eventId}`,
        { method: "DELETE" }
      );
      const data = await res.json();
      if (!res.ok) {
        setError(data.error || "Delete failed");
      } else {
        navigate("/events");
      }
    } catch (err) {
      setError("Failed to delete event");
      console.error(err);
    }
  };

  const inputStyle = { width: "100%", marginTop: "0.5rem" };
  const fieldWrapper = { marginBottom: "1.5rem" };
  const buttonStyle = {
    padding: "8px 16px",
    backgroundColor: "white",
    color: "black",
    border: "2px solid black",
    cursor: "pointer",
  };

  return (
    <div style={{ maxWidth: "600px", margin: "2rem auto" }}>
      <h2 style={{ color: "#0b3d91", textAlign: "center" }}>Update Event</h2>
      {error && <p style={{ color: "red", textAlign: "center" }}>{error}</p>}

      <div style={fieldWrapper}>
        <label>Type</label>
        <input
          type="text"
          name="event_type"
          value={eventData.event_type}
          onChange={handleChange}
          style={inputStyle}
        />
      </div>

      <div style={fieldWrapper}>
        <label>Scheduled At</label>
        <input
          type="datetime-local"
          name="scheduled_at"
          value={eventData.scheduled_at}
          onChange={handleChange}
          style={inputStyle}
        />
      </div>

      <div style={fieldWrapper}>
        <label>Status</label>
        <select
          name="status"
          value={eventData.status}
          onChange={handleChange}
          style={inputStyle}
        >
          <option value="Scheduled">Scheduled</option>
          <option value="Completed">Completed</option>
          <option value="Cancelled">Cancelled</option>
        </select>
      </div>

      <div style={fieldWrapper}>
        <label>Patient ID</label>
        <input
          type="number"
          name="patient_id"
          value={eventData.patient_id}
          onChange={handleChange}
          style={inputStyle}
        />
      </div>

      <div style={fieldWrapper}>
        <label>Doctor ID</label>
        <input
          type="number"
          name="doctor_id"
          value={eventData.doctor_id}
          onChange={handleChange}
          style={inputStyle}
        />
      </div>

      <div style={fieldWrapper}>
        <label>Payment Amount</label>
        <input
          type="number"
          name="payment_amount"
          value={eventData.payment_amount}
          onChange={handleChange}
          style={inputStyle}
        />
      </div>

      <div style={fieldWrapper}>
        <label>Payment Method</label>
        <input
          type="text"
          name="payment_method"
          value={eventData.payment_method}
          onChange={handleChange}
          style={inputStyle}
        />
      </div>

      <div style={fieldWrapper}>
        <label>Description</label>
        <textarea
          name="description"
          value={eventData.description}
          onChange={handleChange}
          style={{ ...inputStyle, height: "120px" }}
        />
      </div>

      <div style={{ display: "flex", justifyContent: "center", gap: "16px" }}>
        <button
          onClick={handleUpdate}
          style={buttonStyle}
          onMouseOver={(e) => {
            e.target.style.backgroundColor = "black";
            e.target.style.color = "white";
          }}
          onMouseOut={(e) => {
            e.target.style.backgroundColor = "white";
            e.target.style.color = "black";
          }}
        >
          Update
        </button>
        <button
          onClick={handleDelete}
          style={buttonStyle}
          onMouseOver={(e) => {
            e.target.style.backgroundColor = "black";
            e.target.style.color = "white";
          }}
          onMouseOut={(e) => {
            e.target.style.backgroundColor = "white";
            e.target.style.color = "black";
          }}
        >
          Delete
        </button>
      </div>
    </div>
  );
};

export default UpdateEvent;
