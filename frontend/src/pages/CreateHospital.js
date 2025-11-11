import React, { useState } from "react";
import { useNavigate } from "react-router-dom";

const CreateHospital = () => {
  const navigate = useNavigate();
  const [hospitalData, setHospitalData] = useState({
    name: "",
    address: "",
    phone: "",
    email: "",
    website: "",
    departments: {
      emergency: false,
      pediatrics: false,
      cardiology: false,
      oncology: false,
      neurology: false,
      orthopedics: false,
      radiology: false,
      maternity: false,
    },
  });
  const [error, setError] = useState("");

  const handleChange = (e) => {
    const { name, value, type, checked } = e.target;
    if (type === "checkbox") {
      setHospitalData({
        ...hospitalData,
        departments: { ...hospitalData.departments, [name]: checked },
      });
    } else {
      setHospitalData({ ...hospitalData, [name]: value });
    }
  };

  const handleCreate = async () => {
    setError("");
    try {
      const res = await fetch(
        "http://127.0.0.1:5000/api/hospital/create_hospital",
        {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify(hospitalData), // send entire object including departments
        }
      );
      const data = await res.json();
      if (!res.ok) {
        setError(data.error || "Create failed");
      } else {
        navigate("/resources");
      }
    } catch (err) {
      setError("Failed to create hospital");
      console.error(err);
    }
  };

  return (
    <div style={{ maxWidth: "600px", margin: "2rem auto" }}>
      <h2 style={{ color: "#0b3d91", textAlign: "center" }}>Create Hospital</h2>
      {error && <p style={{ color: "red", textAlign: "center" }}>{error}</p>}

      <div style={{ marginBottom: "1.5rem" }}>
        <label>Name</label>
        <input
          type="text"
          name="name"
          value={hospitalData.name}
          onChange={handleChange}
          style={{ width: "100%", marginTop: "0.5rem" }}
        />
      </div>

      <div style={{ marginBottom: "1.5rem" }}>
        <label>Address</label>
        <input
          type="text"
          name="address"
          value={hospitalData.address}
          onChange={handleChange}
          style={{ width: "100%", marginTop: "0.5rem" }}
        />
      </div>

      <div style={{ marginBottom: "1.5rem" }}>
        <label>Phone</label>
        <input
          type="text"
          name="phone"
          value={hospitalData.phone}
          onChange={handleChange}
          style={{ width: "100%", marginTop: "0.5rem" }}
        />
      </div>

      <div style={{ marginBottom: "1.5rem" }}>
        <label>Email</label>
        <input
          type="email"
          name="email"
          value={hospitalData.email}
          onChange={handleChange}
          style={{ width: "100%", marginTop: "0.5rem" }}
        />
      </div>

      <div style={{ marginBottom: "1.5rem" }}>
        <label>Website</label>
        <input
          type="text"
          name="website"
          value={hospitalData.website}
          onChange={handleChange}
          style={{ width: "100%", marginTop: "0.5rem" }}
        />
      </div>

      <div style={{ marginBottom: "1.5rem" }}>
        <label>Departments</label>
        <div style={{ marginTop: "0.5rem" }}>
          {Object.keys(hospitalData.departments).map((dep) => (
            <div key={dep} style={{ marginBottom: "0.25rem" }}>
              <input
                type="checkbox"
                name={dep}
                checked={hospitalData.departments[dep]}
                onChange={handleChange}
              />
              <label style={{ marginLeft: "0.5rem" }}>
                {dep.charAt(0).toUpperCase() + dep.slice(1)}
              </label>
            </div>
          ))}
        </div>
      </div>

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

export default CreateHospital;
