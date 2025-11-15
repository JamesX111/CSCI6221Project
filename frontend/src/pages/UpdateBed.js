import React, { useEffect, useState } from "react";
import { useNavigate, useParams } from "react-router-dom";

const UpdateBed = () => {
  const navigate = useNavigate();
  const { bedId } = useParams(); // Only bedId is route param

  const [bedData, setBedData] = useState({
    ward: "emergency",
    status: "unoccupied",
    hospital_id: null, // will be populated from backend
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

  // Fetch existing bed data
  useEffect(() => {
    const fetchBed = async () => {
      try {
        const res = await fetch(
          `http://127.0.0.1:5000/api/hospital/get_bed/${bedId}`,
          { method: "POST" }
        );
        const data = await res.json();
        if (!res.ok || data.error) {
          setError(data.error || "Failed to load bed data");
        } else {
          setBedData({
            ward: data.ward || "emergency",
            status: data.status || "unoccupied",
            hospital_id: data.hospital_id || null,
          });
        }
      } catch (err) {
        console.error(err);
        setError("Failed to load bed data");
      }
    };
    fetchBed();
  }, [bedId]);

  const handleChange = (e) => {
    const { name, value } = e.target;
    setBedData({ ...bedData, [name]: value });
  };

  const handleUpdate = async () => {
    setError("");
    try {
      const res = await fetch(
        `http://127.0.0.1:5000/api/hospital/update_bed/${bedId}`,
        {
          method: "PUT",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({
            ward: bedData.ward,
            status: bedData.status,
          }),
        }
      );
      const data = await res.json();
      if (!res.ok) {
        setError(data.error || "Update failed");
      } else {
        navigate(`/update-hospital/${bedData.hospital_id}`);
      }
    } catch (err) {
      console.error(err);
      setError("Failed to update bed");
    }
  };

  const handleDelete = async () => {
    if (!window.confirm("Are you sure you want to delete this bed?")) return;
    setError("");
    try {
      const res = await fetch(
        `http://127.0.0.1:5000/api/hospital/delete_bed/${bedId}`,
        { method: "DELETE" }
      );
      const data = await res.json();
      if (!res.ok) {
        setError(data.error || "Delete failed");
      } else {
        navigate(`/update-hospital/${bedData.hospital_id}`);
      }
    } catch (err) {
      console.error(err);
      setError("Failed to delete bed");
    }
  };

  return (
    <div style={{ maxWidth: "600px", margin: "2rem auto" }}>
      <h2 style={{ color: "#0b3d91", textAlign: "center" }}>Update Bed</h2>

      <p style={{ textAlign: "center", fontWeight: "bold" }}>
        Hospital ID: {bedData.hospital_id} | Bed ID: {bedId}
      </p>

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

      {/* Buttons */}
      <div style={{ display: "flex", justifyContent: "center", gap: "12px" }}>
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
            backgroundColor: "white",
            color: "red",
            border: "2px solid red",
            cursor: "pointer",
          }}
          onMouseOver={(e) => {
            e.target.style.backgroundColor = "red";
            e.target.style.color = "white";
          }}
          onMouseOut={(e) => {
            e.target.style.backgroundColor = "white";
            e.target.style.color = "red";
          }}
        >
          Delete
        </button>
      </div>
    </div>
  );
};

export default UpdateBed;
