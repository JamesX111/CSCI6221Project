import React, { useState } from "react";
import { useNavigate, useParams } from "react-router-dom";

const CreateBed = () => {
  const navigate = useNavigate();
  const { hospitalId } = useParams();

  const [bedData, setBedData] = useState({
    ward: "emergency", // default value
    status: "unoccupied",
  });

  const [error, setError] = useState("");

  const wards = [
    "emergency",
    "pediatrics",
    "cardiology",
    "oncology",
    "neurology",
    "orthopedics",
    "radiology",
    "maternity",
  ];

  const handleChange = (e) => {
    const { name, value } = e.target;
    setBedData({ ...bedData, [name]: value });
  };

  const handleCreate = async () => {
    setError("");

    try {
      const res = await fetch(
        `http://127.0.0.1:5000/api/hospital/create_bed/${hospitalId}`,
        {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify(bedData),
        }
      );

      const data = await res.json();

      if (!res.ok) {
        setError(data.error || "Create failed");
      } else {
        navigate(`/update-hospital/${hospitalId}`);
      }
    } catch (err) {
      setError("Failed to create bed");
      console.error(err);
    }
  };

  return (
    <div style={{ maxWidth: "600px", margin: "2rem auto" }}>
      <h2 style={{ color: "#0b3d91", textAlign: "center" }}>Create Bed</h2>
      {error && <p style={{ color: "red", textAlign: "center" }}>{error}</p>}

      {/* Ward Dropdown */}
      <div style={{ marginBottom: "1.5rem" }}>
        <label>Ward</label>
        <select
          name="ward"
          value={bedData.ward}
          onChange={handleChange}
          style={{ width: "100%", marginTop: "0.5rem", padding: "6px" }}
        >
          {wards.map((ward) => (
            <option key={ward} value={ward}>
              {ward.charAt(0).toUpperCase() + ward.slice(1)}
            </option>
          ))}
        </select>
      </div>

      {/* Status Dropdown */}
      <div style={{ marginBottom: "1.5rem" }}>
        <label>Status</label>
        <select
          name="status"
          value={bedData.status}
          onChange={handleChange}
          style={{ width: "100%", marginTop: "0.5rem", padding: "6px" }}
        >
          <option value="occupied">Occupied</option>
          <option value="unoccupied">Unoccupied</option>
        </select>
      </div>

      {/* Create Button */}
      <div style={{ display: "flex", justifyContent: "center" }}>
        <button
          onClick={handleCreate}
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
          Create
        </button>
      </div>
    </div>
  );
};

export default CreateBed;
