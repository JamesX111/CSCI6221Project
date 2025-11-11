import React, { useEffect, useState } from "react";
import { useParams, useNavigate } from "react-router-dom";

const UpdateAccident = () => {
  const { id } = useParams();
  const navigate = useNavigate();
  const [accidentData, setAccidentData] = useState({
    accident_type: "",
    description: "",
    occurred_at: "",
    severity: "Low",
    location: "",
    patient_id: "",
  });
  const [error, setError] = useState("");

  useEffect(() => {
    // Fetch the existing accident data
    fetch(`http://127.0.0.1:5000/api/accidents/get_all`, { method: "POST" })
      .then((res) => res.json())
      .then((data) => {
        const accident = data.find((a) => a.id === parseInt(id));
        if (accident) {
          setAccidentData({
            accident_type: accident.accident_type || "",
            description: accident.description || "",
            occurred_at: accident.occurred_at || "",
            severity: accident.severity || "Low",
            location: accident.location || "",
            patient_id: accident.patient ? accident.patient.id : "",
          });
        }
      })
      .catch((err) => console.error(err));
  }, [id]);

  const handleChange = (e) => {
    setAccidentData({ ...accidentData, [e.target.name]: e.target.value });
  };

  const handleUpdate = async () => {
    setError("");
    try {
      const res = await fetch(
        `http://127.0.0.1:5000/api/accidents/update_accident/${id}`,
        {
          method: "PUT",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify(accidentData),
        }
      );
      const data = await res.json();
      if (!res.ok) {
        setError(data.error || "Update failed");
      } else {
        navigate("/accidents");
      }
    } catch (err) {
      setError("Failed to update accident");
      console.error(err);
    }
  };

  const handleDelete = async () => {
    setError("");
    try {
      const res = await fetch(
        `http://127.0.0.1:5000/api/accidents/delete_accident/${id}`,
        { method: "DELETE" }
      );
      const data = await res.json();
      if (!res.ok) {
        setError(data.error || "Delete failed");
      } else {
        navigate("/accidents");
      }
    } catch (err) {
      setError("Failed to delete accident");
      console.error(err);
    }
  };

  return (
    <div style={{ maxWidth: "600px", margin: "2rem auto" }}>
      <h2 style={{ color: "#0b3d91", textAlign: "center" }}>Update Accident</h2>
      {error && <p style={{ color: "red", textAlign: "center" }}>{error}</p>}

      <div style={{ marginBottom: "1.5rem" }}>
        <label>Type</label>
        <input
          type="text"
          name="accident_type"
          value={accidentData.accident_type}
          onChange={handleChange}
          style={{ width: "100%", marginTop: "0.5rem" }}
        />
      </div>

      <div style={{ marginBottom: "1.5rem" }}>
        <label>Occurred At</label>
        <input
          type="datetime-local"
          name="occurred_at"
          value={accidentData.occurred_at.slice(0, 16)}
          onChange={handleChange}
          style={{ width: "100%", marginTop: "0.5rem" }}
        />
      </div>

      <div style={{ marginBottom: "1.5rem" }}>
        <label>Severity</label>
        <select
          name="severity"
          value={accidentData.severity}
          onChange={handleChange}
          style={{ width: "100%", marginTop: "0.5rem" }}
        >
          <option value="Low">Low</option>
          <option value="Moderate">Moderate</option>
          <option value="Severe">Severe</option>
        </select>
      </div>

      <div style={{ marginBottom: "1.5rem" }}>
        <label>Location</label>
        <input
          type="text"
          name="location"
          value={accidentData.location}
          onChange={handleChange}
          style={{ width: "100%", marginTop: "0.5rem" }}
        />
      </div>

      <div style={{ marginBottom: "1.5rem" }}>
        <label>Patient ID</label>
        <input
          type="number"
          name="patient_id"
          value={accidentData.patient_id}
          onChange={handleChange}
          style={{ width: "100%", marginTop: "0.5rem" }}
        />
      </div>

      <div style={{ marginBottom: "1.5rem" }}>
        <label>Description</label>
        <textarea
          name="description"
          value={accidentData.description}
          onChange={handleChange}
          style={{ width: "100%", height: "120px", marginTop: "0.5rem" }}
        />
      </div>

      <div style={{ display: "flex", justifyContent: "center", gap: "1rem" }}>
        <button
          onClick={handleUpdate}
          style={{
            padding: "8px 16px",
            backgroundColor: "white",
            color: "black",
            border: "2px solid black",
            cursor: "pointer",
          }}
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
          style={{
            padding: "8px 16px",
            backgroundColor: "red",
            color: "white",
            border: "2px solid black",
            cursor: "pointer",
          }}
          onMouseOver={(e) => {
            e.target.style.backgroundColor = "darkred";
          }}
          onMouseOut={(e) => {
            e.target.style.backgroundColor = "red";
          }}
        >
          Delete
        </button>
      </div>
    </div>
  );
};

export default UpdateAccident;
