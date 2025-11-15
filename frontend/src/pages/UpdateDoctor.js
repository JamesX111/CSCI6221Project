import React, { useEffect, useState } from "react";
import { useNavigate, useParams } from "react-router-dom";

const UpdateDoctor = () => {
  const { doctorId } = useParams();
  const navigate = useNavigate();

  const [doctorData, setDoctorData] = useState({
    name: "",
    email: "",
    phone: "",
    specialty: "",
    department: "emergency",
    available: true, // ✅ use key 'available'
  });
  const [hospitalId, setHospitalId] = useState(null);
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

  useEffect(() => {
    const fetchDoctor = async () => {
      try {
        const res = await fetch(
          `http://127.0.0.1:5000/api/hospital/get_doctor/${doctorId}`,
          { method: "POST" }
        );
        const data = await res.json();
        if (!res.ok && data.error) {
          setError(data.error);
        } else {
          setDoctorData({
            name: data.name || "",
            email: data.email || "",
            phone: data.phone || "",
            specialty: data.specialty || "",
            department: data.department || "emergency",
            available: data.available ?? true, // ✅ match backend key
          });
          setHospitalId(data.hospital?.id || null);
        }
      } catch (err) {
        setError("Failed to load doctor");
        console.error(err);
      }
    };
    fetchDoctor();
  }, [doctorId]);

  const handleChange = (e) => {
    const { name, value } = e.target;
    if (name === "available") {
      setDoctorData({ ...doctorData, available: value === "true" }); // convert to boolean
    } else {
      setDoctorData({ ...doctorData, [name]: value });
    }
  };

  const handleUpdate = async () => {
    setError("");
    try {
      const res = await fetch(
        `http://127.0.0.1:5000/api/hospital/update_doctor/${doctorId}`,
        {
          method: "PUT",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify(doctorData), // sends available as boolean
        }
      );
      const data = await res.json();
      if (!res.ok) {
        setError(data.error || "Update failed");
      } else {
        if (hospitalId) navigate(`/update-hospital/${hospitalId}`);
      }
    } catch (err) {
      setError("Failed to update doctor");
      console.error(err);
    }
  };

  const handleDelete = async () => {
    if (!window.confirm("Are you sure you want to delete this doctor?")) return;
    try {
      const res = await fetch(
        `http://127.0.0.1:5000/api/hospital/delete_doctor/${doctorId}`,
        { method: "DELETE" }
      );
      const data = await res.json();
      if (!res.ok) {
        setError(data.error || "Delete failed");
      } else {
        if (hospitalId) navigate(`/update-hospital/${hospitalId}`);
      }
    } catch (err) {
      setError("Failed to delete doctor");
      console.error(err);
    }
  };

  return (
    <div style={{ maxWidth: "600px", margin: "2rem auto" }}>
      <h2 style={{ color: "#0b3d91", textAlign: "center" }}>Update Doctor</h2>
      {hospitalId && (
        <p style={{ textAlign: "center", marginBottom: "1rem" }}>
          Hospital ID: {hospitalId}
        </p>
      )}
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

      {/* Department */}
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

      {/* Availability */}
      <div style={{ marginBottom: "1.5rem" }}>
        <label>Availability</label>
        <select
          name="available"
          value={doctorData.available ? "true" : "false"}
          onChange={handleChange}
          style={{ width: "100%", marginTop: "0.5rem", padding: "6px" }}
        >
          <option value="true">Available</option>
          <option value="false">Unavailable</option>
        </select>
      </div>

      {/* Buttons */}
      <div style={{ display: "flex", justifyContent: "center", gap: "16px" }}>
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
          Delete
        </button>
      </div>
    </div>
  );
};

export default UpdateDoctor;
