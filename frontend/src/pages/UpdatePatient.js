import React, { useEffect, useState } from "react";
import { useNavigate, useParams } from "react-router-dom";
import Table from "react-bootstrap/Table";

const UpdatePatient = () => {
  const { patientId } = useParams();
  const navigate = useNavigate();

  const [patientData, setPatientData] = useState({
    FName: "",
    LName: "",
    Gender: "",
    Date_Of_Birth: "",
    contact_No: "",
    pt_Address: "",
  });

  const [medicalRecords, setMedicalRecords] = useState([]);
  const [error, setError] = useState("");

  // Fetch patient
  useEffect(() => {
    const fetchPatient = async () => {
      try {
        const res = await fetch(
          `http://127.0.0.1:5000/api/patients/get/${patientId}`,
          { method: "POST" }
        );
        const data = await res.json();

        if (!res.ok) {
          setError(data.error || "Failed to load patient");
        } else {
          setPatientData({
            FName: data.FName || "",
            LName: data.LName || "",
            Gender: data.Gender || "",
            Date_Of_Birth: data.Date_Of_Birth || "",
            contact_No: data.contact_No || "",
            pt_Address: data.pt_Address || "",
          });
        }
      } catch (err) {
        setError("Failed to load patient");
      }
    };

    fetchPatient();
  }, [patientId]);

  // Fetch medical records
  useEffect(() => {
    const fetchMedicalRecords = async () => {
      try {
        const res = await fetch(
          `http://127.0.0.1:5000/api/medical_records/get_by_patient/${patientId}`
        );

        const data = await res.json();

        if (!res.ok) {
          console.error(data.error);
        } else {
          setMedicalRecords(data || []);
        }
      } catch (err) {
        console.error("Failed to load medical records");
      }
    };

    fetchMedicalRecords();
  }, [patientId]);

  // Form handlers
  const handleChange = (e) => {
    const { name, value } = e.target;
    setPatientData({ ...patientData, [name]: value });
  };

  const handleUpdate = async () => {
    setError("");
    try {
      const res = await fetch(
        `http://127.0.0.1:5000/api/patients/update/${patientId}`,
        {
          method: "PUT",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify(patientData),
        }
      );

      const data = await res.json();
      if (!res.ok) setError(data.error || "Update failed");
      else navigate("/patients");
    } catch (err) {
      setError("Failed to update patient");
    }
  };

  const handleDelete = async () => {
    if (!window.confirm("Are you sure you want to delete this patient?")) return;

    try {
      const res = await fetch(
        `http://127.0.0.1:5000/api/patients/delete/${patientId}`,
        { method: "DELETE" }
      );

      const data = await res.json();
      if (!res.ok) setError(data.error || "Delete failed");
      else navigate("/patients");
    } catch (err) {
      setError("Failed to delete patient");
    }
  };

  return (
    <div style={{ maxWidth: "800px", margin: "2rem auto" }}>
      <h2 style={{ color: "#0b3d91", textAlign: "center" }}>Update Patient</h2>

      {error && <p style={{ color: "red", textAlign: "center" }}>{error}</p>}

      {/* FORM FIELDS */}
      <div style={{ marginBottom: "1.5rem" }}>
        <label>First Name</label>
        <input
          type="text"
          name="FName"
          value={patientData.FName}
          onChange={handleChange}
          style={{ width: "100%", marginTop: "0.5rem" }}
        />
      </div>

      <div style={{ marginBottom: "1.5rem" }}>
        <label>Last Name</label>
        <input
          type="text"
          name="LName"
          value={patientData.LName}
          onChange={handleChange}
          style={{ width: "100%", marginTop: "0.5rem" }}
        />
      </div>

      <div style={{ marginBottom: "1.5rem" }}>
        <label>Gender</label>
        <select
          name="Gender"
          value={patientData.Gender}
          onChange={handleChange}
          style={{ width: "100%", marginTop: "0.5rem", padding: "6px" }}
        >
          <option value="">Select Gender</option>
          <option value="Male">Male</option>
          <option value="Female">Female</option>
          <option value="Other">Other</option>
        </select>
      </div>

      <div style={{ marginBottom: "1.5rem" }}>
        <label>Date of Birth</label>
        <input
          type="date"
          name="Date_Of_Birth"
          value={patientData.Date_Of_Birth}
          onChange={handleChange}
          style={{ width: "100%", marginTop: "0.5rem" }}
        />
      </div>

      <div style={{ marginBottom: "1.5rem" }}>
        <label>Contact Number</label>
        <input
          type="text"
          name="contact_No"
          value={patientData.contact_No}
          onChange={handleChange}
          style={{ width: "100%", marginTop: "0.5rem" }}
        />
      </div>

      <div style={{ marginBottom: "1.5rem" }}>
        <label>Address</label>
        <textarea
          name="pt_Address"
          value={patientData.pt_Address}
          onChange={handleChange}
          style={{ width: "100%", marginTop: "0.5rem", height: "80px" }}
        />
      </div>

      {/* BUTTONS */}
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

      {/* ============================== */}
      {/* MEDICAL RECORDS TABLE SECTION */}
      {/* ============================== */}

      <h3 style={{ marginTop: "3rem", textAlign: "center", color: "#0b3d91" }}>
  Medical Records
</h3>

<Table
  bordered
  hover
  style={{
    width: "100%",
    tableLayout: "fixed", // Makes columns evenly spaced
    wordWrap: "break-word",
  }}
>
  <thead style={{ backgroundColor: "#f5f5f5" }}>
    <tr>
      <th style={{ width: "6%" }}>ID</th>
      <th style={{ width: "12%" }}>Doctor</th>
      <th style={{ width: "10%" }}>Visit Date</th>
      <th style={{ width: "7%" }}>Weight</th>
      <th style={{ width: "7%" }}>Height</th>
      <th style={{ width: "8%" }}>BP</th>
      <th style={{ width: "8%" }}>Temp (°F)</th>
      <th style={{ width: "20%" }}>Diagnosis</th>
      <th style={{ width: "20%" }}>Treatment</th>
      <th style={{ width: "12%" }}>Next Visit</th>
    </tr>
  </thead>

  <tbody>
    {medicalRecords.length === 0 ? (
      <tr>
        <td colSpan="10" style={{ textAlign: "center", padding: "12px" }}>
          No medical records found.
        </td>
      </tr>
    ) : (
      medicalRecords.map((rec) => (
        <tr key={rec.record_Id}>
          <td style={{ padding: "10px" }}>{rec.record_Id}</td>
          <td style={{ padding: "10px" }}>{rec.doctor_Name}</td>
          <td style={{ padding: "10px" }}>
            {rec.visit_Date?.split("T")[0]}
          </td>
          <td style={{ padding: "10px" }}>{rec.curr_Weight || "—"}</td>
          <td style={{ padding: "10px" }}>{rec.curr_height || "—"}</td>
          <td style={{ padding: "10px" }}>{rec.curr_Blood_Pressure || "—"}</td>
          <td style={{ padding: "10px" }}>{rec.curr_Temp_F || "—"}</td>
          <td style={{ padding: "10px", whiteSpace: "pre-wrap" }}>
            {rec.diagnosis || "—"}
          </td>
          <td style={{ padding: "10px", whiteSpace: "pre-wrap" }}>
            {rec.treatment || "—"}
          </td>
          <td style={{ padding: "10px" }}>
            {rec.next_Visit?.split("T")[0] || "—"}
          </td>
        </tr>
      ))
    )}
  </tbody>
</Table>

    </div>
  );
};

export default UpdatePatient;
