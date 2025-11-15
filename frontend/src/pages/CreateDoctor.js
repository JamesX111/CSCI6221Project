import React, { useState } from "react";
import { useNavigate, useParams } from "react-router-dom";

const CreateDoctor = () => {
  const navigate = useNavigate();
  const { hospitalId } = useParams();

  const [doctorData, setDoctorData] = useState({
    name: "",
    email: "",
    phone: "",
    specialty: "",
    department: "emergency",
    available: true,
  });

  const [error, setError] = useState("");

  const departments = [
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
    setDoctorData({ ...doctorData, [name]: value });
  };

  const handleCreate = async () => {
    setError("");
    try {
      const res = await fetch(
        `http://127.0.0.1:5000/api/hospital/create_doctor/${hospitalId}`,
        {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify(doctorData),
        }
      );

      const data = await res.json();

      if (!res.ok) {
        setError(data.error || "Create failed");
      } else {
        navigate(`/update-hospital/${hospitalId}`);
      }
    } catch (err) {
      console.error(err);
      setError("Failed to create doctor");
    }
  };

  return (
    <div style={{ maxWidth: "600px", margin: "2rem auto" }}>
      <h2 style={{ color: "#0b3d91", textAlign: "center" }}>Create Doctor</h2>
      {error && <p style={{ color: "red", textAlign: "center" }}>{error}</p>}

      {/* Name */}
      <div style={{ marginBottom: "1.5rem" }}>
        <label>Name</label>
        <input
          type="text"
          name="name"
          value={doctorData.name}
          onChange={handleChange}
          style={{ width: "100%", marginTop: "0.5rem" }}
        />
      </div>

      {/* Email */}
      <div style={{ marginBottom: "1.5rem" }}>
        <label>Email</label>
        <input
          type="email"
          name="email"
          value={doctorData.email}
          onChange={handleChange}
          style={{ width: "100%", marginTop: "0.5rem" }}
        />
      </div>

      {/* Phone */}
      <div style={{ marginBottom: "1.5rem" }}>
        <label>Phone</label>
        <input
          type="text"
          name="phone"
          value={doctorData.phone}
          onChange={handleChange}
          style={{ width: "100%", marginTop: "0.5rem" }}
        />
      </div>

      {/* Specialty */}
      <div style={{ marginBottom: "1.5rem" }}>
        <label>Specialty</label>
        <input
          type="text"
          name="specialty"
          value={doctorData.specialty}
          onChange={handleChange}
          style={{ width: "100%", marginTop: "0.5rem" }}
        />
      </div>

      {/* Department Dropdown */}
      <div style={{ marginBottom: "1.5rem" }}>
        <label>Department</label>
        <select
          name="department"
          value={doctorData.department}
          onChange={handleChange}
          style={{ width: "100%", marginTop: "0.5rem", padding: "6px" }}
        >
          {departments.map((dep) => (
            <option key={dep} value={dep}>
              {dep.charAt(0).toUpperCase() + dep.slice(1)}
            </option>
          ))}
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

export default CreateDoctor;
