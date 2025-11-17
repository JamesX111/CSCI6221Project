import React, { useEffect, useState } from "react";
import { Table, Button } from "react-bootstrap";
import { useNavigate } from "react-router-dom";

const Resources = () => {
  const [doctors, setDoctors] = useState([]);
  const [wards, setWards] = useState([]);
  const navigate = useNavigate();

  useEffect(() => {
    fetch("http://127.0.0.1:5000/api/doctors/get_all", { method: "POST" })
      .then((res) => res.json())
      .then((data) => setDoctors(data))
      .catch((err) => console.error(err));

    fetch("http://127.0.0.1:5000/api/wards/get_all", { method: "POST" })
      .then((res) => res.json())
      .then((data) => setWards(data))
      .catch((err) => console.error(err));
  }, []);

  const tableStyle = {
    borderCollapse: "separate",
    borderSpacing: "0 8px",
    tableLayout: "fixed",
    width: "100%",
  };

  const thTdStyleDoctors = {
    width: `${100 / 8}%`,
    textAlign: "center",
    wordWrap: "break-word",
  };

  const thTdStyleWards = {
    width: `${100 / 3}%`,
    textAlign: "center",
    wordWrap: "break-word",
  };

  const rowHoverStyle = (e) => (e.currentTarget.style.backgroundColor = "#f0f6ff");
  const rowNormalStyle = (e) => (e.currentTarget.style.backgroundColor = "transparent");

  return (
    <div style={{ padding: "2rem" }}>
      {/* Doctors Section */}
      <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", marginBottom: "1.5rem" }}>
        <h2 style={{ color: "#0b3d91" }}>Doctors</h2>
        <Button
          style={{
            backgroundColor: "white",
            color: "black",
            border: "2px solid black",
            borderRadius: "8px",
            fontWeight: 500,
            padding: "6px 16px",
            transition: "all 0.25s ease-in-out",
          }}
          onMouseOver={(e) => { e.target.style.backgroundColor = "black"; e.target.style.color = "white"; }}
          onMouseOut={(e) => { e.target.style.backgroundColor = "white"; e.target.style.color = "black"; }}
          onClick={() => navigate("/create-doctor")}
        >
          Add Doctor
        </Button>
      </div>

      <Table striped bordered hover style={tableStyle}>
        <thead>
          <tr>
            <th style={thTdStyleDoctors}>ID</th>
            <th style={thTdStyleDoctors}>First Name</th>
            <th style={thTdStyleDoctors}>Last Name</th>
            <th style={thTdStyleDoctors}>Gender</th>
            <th style={thTdStyleDoctors}>Contact</th>
            <th style={thTdStyleDoctors}>Department</th>
            <th style={thTdStyleDoctors}>Surgeon Type</th>
            <th style={thTdStyleDoctors}>Office No</th>
          </tr>
        </thead>
        <tbody>
          {doctors.map((d) => (
            <tr
              key={d.doct_Id}
              style={{ cursor: "pointer" }}
              onClick={() => navigate(`/update-doctor/${d.doct_Id}`)}
              onMouseOver={rowHoverStyle}
              onMouseOut={rowNormalStyle}
            >
              <td style={thTdStyleDoctors}>{d.doct_Id}</td>
              <td style={thTdStyleDoctors}>{d.FName}</td>
              <td style={thTdStyleDoctors}>{d.LName}</td>
              <td style={thTdStyleDoctors}>{d.Gender}</td>
              <td style={thTdStyleDoctors}>{d.contact_No || "—"}</td>
              <td style={thTdStyleDoctors}>{d.dept_Name || "—"}</td>
              <td style={thTdStyleDoctors}>{d.surgeon_Type || "—"}</td>
              <td style={thTdStyleDoctors}>{d.office_No || "—"}</td>
            </tr>
          ))}
        </tbody>
      </Table>

      {/* Wards Section */}
      <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", margin: "2rem 0 1.5rem 0" }}>
        <h2 style={{ color: "#0b3d91" }}>Wards</h2>
        <Button
          style={{
            backgroundColor: "white",
            color: "black",
            border: "2px solid black",
            borderRadius: "8px",
            fontWeight: 500,
            padding: "6px 16px",
            transition: "all 0.25s ease-in-out",
          }}
          onMouseOver={(e) => { e.target.style.backgroundColor = "black"; e.target.style.color = "white"; }}
          onMouseOut={(e) => { e.target.style.backgroundColor = "white"; e.target.style.color = "black"; }}
          onClick={() => navigate("/create-ward")}
        >
          Add Ward
        </Button>
      </div>

      <Table striped bordered hover style={tableStyle}>
        <thead>
          <tr>
            <th style={thTdStyleWards}>Ward No</th>
            <th style={thTdStyleWards}>Ward Name</th>
            <th style={thTdStyleWards}>Department</th>
          </tr>
        </thead>
        <tbody>
          {wards.map((w) => (
            <tr
              key={w.ward_No}
              style={{ cursor: "pointer" }}
              onClick={() => navigate(`/update-ward/${w.ward_No}`)}
              onMouseOver={rowHoverStyle}
              onMouseOut={rowNormalStyle}
            >
              <td style={thTdStyleWards}>{w.ward_No}</td>
              <td style={thTdStyleWards}>{w.ward_Name}</td>
              <td style={thTdStyleWards}>{w.dept_Name || "—"}</td>
            </tr>
          ))}
        </tbody>
      </Table>
    </div>
  );
};

export default Resources;
