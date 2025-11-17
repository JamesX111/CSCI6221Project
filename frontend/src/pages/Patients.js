import React, { useEffect, useState } from "react";
import { Table, Button } from "react-bootstrap";
import { useNavigate } from "react-router-dom";

const Patients = () => {
  const [patients, setPatients] = useState([]);
  const navigate = useNavigate();

  const fetchPatients = async () => {
    try {
      const res = await fetch("http://127.0.0.1:5000/api/patients/get_all", { method: "POST" });
      const data = await res.json();
      setPatients(data);
    } catch (err) {
      console.error(err);
    }
  };

  useEffect(() => {
    fetchPatients();
  }, []);

  return (
    <div className="patients-page" style={{ padding: "2rem" }}>
      <div
        className="patients-header"
        style={{
          display: "flex",
          justifyContent: "space-between",
          alignItems: "center",
          marginBottom: "1.5rem",
        }}
      >
        <h2 style={{ color: "#0b3d91" }}>Patients</h2>
        <Button
          className="add-patient-btn"
          onClick={() => navigate("/create-patient")}
          style={{
            backgroundColor: "white",
            color: "black",
            border: "2px solid black",
            borderRadius: "8px",
            padding: "6px 16px",
            fontWeight: 500,
            transition: "all 0.25s ease-in-out",
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
          Create Patient
        </Button>
      </div>

      <Table
        striped
        bordered
        hover
        className="patients-table"
        style={{ borderCollapse: "separate", borderSpacing: "0 8px" }}
      >
        <thead>
          <tr>
            <th style={{ width: "5%" }}>ID</th>
            <th style={{ width: "15%" }}>First Name</th>
            <th style={{ width: "15%" }}>Last Name</th>
            <th style={{ width: "10%" }}>Gender</th>
            <th style={{ width: "10%" }}>Date of Birth</th>
            <th style={{ width: "15%" }}>Contact No</th>
            <th style={{ width: "30%" }}>Address</th>
          </tr>
        </thead>
        <tbody>
          {patients.map((p) => (
            <tr
              key={p.patient_Id}
              style={{ cursor: "pointer", transition: "background-color 0.2s" }}
              onClick={() => navigate(`/update-patient/${p.patient_Id}`)}
              onMouseOver={(e) => (e.currentTarget.style.backgroundColor = "#f0f0f0")}
              onMouseOut={(e) => (e.currentTarget.style.backgroundColor = "")}
            >
              <td>{p.patient_Id}</td>
              <td>{p.FName}</td>
              <td>{p.LName}</td>
              <td>{p.Gender}</td>
              <td>{p.Date_Of_Birth}</td>
              <td>{p.contact_No || "—"}</td>
              <td>{p.pt_Address || "—"}</td>
            </tr>
          ))}
        </tbody>
      </Table>
    </div>
  );
};

export default Patients;
