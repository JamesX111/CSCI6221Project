import React, { useEffect, useState } from "react";
import { useNavigate, useParams } from "react-router-dom";

const UpdateHospital = () => {
  const { hospitalId } = useParams();
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
  const [doctors, setDoctors] = useState([]);
  const [bedOccupancy, setBedOccupancy] = useState([]);
  const [error, setError] = useState("");


  useEffect(() => {
    if (!hospitalId) return;
    const fetchHospital = async () => {
      try {
        const res = await fetch(
          `http://127.0.0.1:5000/api/hospital/get_hospital/${hospitalId}`,
          { method: "POST" }
        );
        const data = await res.json();
        if (!res.ok && data.error) {
          setError(data.error);
        } else {
          setHospitalData({
            name: data.name || "",
            address: data.address || "",
            phone: data.phone || "",
            email: data.email || "",
            website: data.website || "",
            departments: data.departments || {
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
        }
      } catch (err) {
        setError("Failed to load hospital");
        console.error(err);
      }
    };
    fetchHospital();

    const fetchBeds = async () => {
      try {
        const res = await fetch(
          `http://127.0.0.1:5000/api/hospital/get_bedding/${hospitalId}`,
          { method: "POST" }
        );
        const data = await res.json();

        if (!data.error) {
          // Map each bed from backend to proper format
          const bedsArray = data.map((bed) => ({
            bed_id: bed.bed_id,
            ward: bed.ward || "Unknown",
            status: bed.status === "Occupied" ? "Occupied" : "Unoccupied",
            last_updated: bed.last_updated
              ? new Date(bed.last_updated).toLocaleString()
              : "N/A",
          }));

          setBedOccupancy(bedsArray);
        } else {
          console.error("Error fetching beds:", data.error);
        }
      } catch (err) {
        console.error("Bed fetch failed", err);
      }
    };


    const fetchDoctors = async () => {
      try {
        const res = await fetch(
          `http://127.0.0.1:5000/api/hospital/get_doctors/${hospitalId}`,
          { method: "POST" }
        );

        const data = await res.json();

        if (!data.error) {
          // Map the returned doctors to the fields we want
          const doctorsArray = data.map((doc) => ({
            id: doc.id,
            name: doc.name,
            specialty: doc.specialty,
            email: doc.email,
            phone: doc.phone,
            department: doc.department,
            hospital_id: doc.hospital?.id || null,
            available: doc.available,
          }));

          setDoctors(doctorsArray);
        }
      } catch (err) {
        console.error("Doctor fetch failed", err);
      }
    };


    fetchBeds();
    fetchDoctors();

  }, [hospitalId]);

  

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

  const handleUpdate = async () => {
    setError("");
    try {
      const res = await fetch(
        `http://127.0.0.1:5000/api/hospital/update_hospital/${hospitalId}`,
        {
          method: "PUT",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify(hospitalData),
        }
      );
      const data = await res.json();
      if (!res.ok) {
        setError(data.error || "Update failed");
      } else {
        navigate("/resources");
      }
    } catch (err) {
      setError("Failed to update hospital");
      console.error(err);
    }
  };

  const handleDelete = async () => {
    if (!window.confirm("Are you sure you want to delete this hospital?")) return;
    try {
      const res = await fetch(
        `http://127.0.0.1:5000/api/hospital/delete_hospital/${hospitalId}`,
        { method: "DELETE" }
      );
      const data = await res.json();
      if (!res.ok) {
        setError(data.error || "Delete failed");
      } else {
        navigate("/resources");
      }
    } catch (err) {
      setError("Failed to delete hospital");
      console.error(err);
    }
  };

  return (
  <div style={{ maxWidth: "600px", margin: "2rem auto" }}>
    <h2 style={{ color: "#0b3d91", textAlign: "center" }}>Update Hospital</h2>
    {error && <p style={{ color: "red", textAlign: "center" }}>{error}</p>}

    {["name", "address", "phone", "email", "website"].map((field) => (
      <div style={{ marginBottom: "1.5rem" }} key={field}>
        <label>{field.charAt(0).toUpperCase() + field.slice(1)}</label>
        <input
          type={field === "email" ? "email" : "text"}
          name={field}
          value={hospitalData[field]}
          onChange={handleChange}
          style={{ width: "100%", marginTop: "0.5rem" }}
        />
      </div>
    ))}

    <div style={{ marginBottom: "1.5rem" }}>
      <label>Departments</label>
      <div style={{ marginTop: "0.5rem" }}>
        {Object.keys(hospitalData.departments).map((dep) => (
          <div key={dep}>
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

    {/* UPDATE + DELETE BUTTONS */}
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

    {/* =============================== */}
    {/*         BED OCCUPANCY TABLE     */}
    {/* =============================== */}
    <h3 style={{ color: "#0b3d91", marginTop: "3rem" }}>Bed Occupancy</h3>

    <button
      style={{
        marginBottom: "0.5rem",
        padding: "6px 12px",
        border: "1px solid black",
        background: "white",
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
      onClick={() => navigate(`/create-bed/${hospitalId}`)} // link to create bed
    >
      Add Bed
    </button>

    <table style={{ width: "100%", borderCollapse: "collapse" }}>
      <thead>
        <tr>
          <th style={{ borderBottom: "2px solid black", padding: "8px" }}>Bed ID</th>
          <th style={{ borderBottom: "2px solid black", padding: "8px" }}>Ward</th>
          <th style={{ borderBottom: "2px solid black", padding: "8px" }}>Status</th>
        </tr>
      </thead>
      <tbody>
        {bedOccupancy && bedOccupancy.length > 0 ? (
          bedOccupancy.map((bed) => (
            <tr
              key={bed.bed_id}
              style={{ cursor: "pointer" }}
              onClick={() => navigate(`/update-bed/${bed.bed_id}`)} // row clickable
            >
              <td style={{ borderBottom: "1px solid #ccc", padding: "8px" }}>{bed.bed_id}</td>
              <td style={{ borderBottom: "1px solid #ccc", padding: "8px" }}>{bed.ward}</td>
              <td style={{ borderBottom: "1px solid #ccc", padding: "8px" }}>{bed.status}</td>
            </tr>
          ))
        ) : (
          <tr>
            <td style={{ padding: "8px", color: "gray" }} colSpan={4}>
              No bed occupancy data available.
            </td>
          </tr>
        )}
      </tbody>
    </table>



    {/* =============================== */}
    {/*            DOCTORS TABLE        */}
    {/* =============================== */}
    <h3 style={{ color: "#0b3d91" }}>Doctors</h3>

    <button
      style={{
        marginBottom: "0.5rem",
        padding: "6px 12px",
        border: "1px solid black",
        background: "white",
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
      onClick={() => navigate(`/create-doctor/${hospitalId}`)}   // ⭐ link added
    >
        Add Doctor
      </button>

      <table style={{ width: "100%", borderCollapse: "collapse" }}>
        <thead>
          <tr>
            <th style={{ borderBottom: "2px solid black", padding: "8px" }}>
              Doctor Name
            </th>
            <th style={{ borderBottom: "2px solid black", padding: "8px" }}>
              Specialty
            </th>
            <th style={{ borderBottom: "2px solid black", padding: "8px" }}>
              Department
            </th>
            <th style={{ borderBottom: "2px solid black", padding: "8px" }}>
              Availability
            </th>
          </tr>
        </thead>
        <tbody>
          {doctors && doctors.length > 0 ? (
            doctors.map((doc) => (
              <tr
                key={doc.id}
                style={{ cursor: "pointer" }}
                onClick={() => navigate(`/update-doctor/${doc.id}`)}   // ⭐ row link added
              >
                <td style={{ borderBottom: "1px solid #ccc", padding: "8px" }}>
                  {doc.name}
                </td>
                <td style={{ borderBottom: "1px solid #ccc", padding: "8px" }}>
                  {doc.specialty}
                </td>
                <td style={{ borderBottom: "1px solid #ccc", padding: "8px" }}>
                  {doc.department.charAt(0).toUpperCase() + doc.department.slice(1)}
                </td>
                <td style={{ borderBottom: "1px solid #ccc", padding: "8px" }}>
                  {doc.available ? "Available" : "Unavailable"}
                </td>
              </tr>
            ))
          ) : (
            <tr>
              <td style={{ padding: "8px", color: "gray" }} colSpan={2}>
                No doctors found.
              </td>
            </tr>
          )}
        </tbody>
      </table>

  </div>
);
};
export default UpdateHospital;
