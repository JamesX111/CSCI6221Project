import React, { useEffect, useState } from "react";
import { Table, Button } from "react-bootstrap";
import { useNavigate } from "react-router-dom";

const Accident = () => {
  const [accidents, setAccidents] = useState([]);
  const navigate = useNavigate();

  const fetchAccidents = async () => {
    try {
      const res = await fetch("http://127.0.0.1:5000/api/accidents/get_all", { method: "POST" });
      const data = await res.json();
      setAccidents(data);
    } catch (err) {
      console.error(err);
    }
  };

  useEffect(() => {
    fetchAccidents();
  }, []);

  return (
    <div className="accidents-page" style={{ padding: "2rem" }}>
      <div
        className="accidents-header"
        style={{ display: "flex", justifyContent: "space-between", alignItems: "center", marginBottom: "1.5rem" }}
      >
        <h2 style={{ color: "#0b3d91" }}>Accidents</h2>
        <Button
          className="add-accident-btn"
          onClick={() => navigate("/create-accident")}
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
          Create Accident
        </Button>
      </div>

      <Table
        striped
        bordered
        hover
        className="accidents-table"
        style={{ borderCollapse: "separate", borderSpacing: "0 8px" }}
      >
        <thead>
          <tr>
            <th style={{ width: "10%" }}>ID</th>
            <th style={{ width: "10%" }}>Type</th>
            <th style={{ width: "40%" }}>Description</th>
            <th style={{ width: "10%" }}>Occurred At</th>
            <th style={{ width: "10%" }}>Severity</th>
            <th style={{ width: "10%" }}>Location</th>
            <th style={{ width: "10%" }}>Patient</th>
          </tr>
        </thead>
        <tbody>
          {accidents.map((acc) => (
            <tr
              key={acc.id}
              style={{ cursor: "pointer", transition: "background-color 0.2s" }}
              onClick={() => navigate(`/update-accident/${acc.id}`)}
              onMouseOver={(e) => (e.currentTarget.style.backgroundColor = "#f0f0f0")}
              onMouseOut={(e) => (e.currentTarget.style.backgroundColor = "")}
            >
              <td style={{ width: "10%" }}>{acc.id}</td>
              <td style={{ width: "10%" }}>{acc.accident_type}</td>
              <td style={{ width: "40%" }}>{acc.description}</td>
              <td style={{ width: "10%" }}>{acc.occurred_at}</td>
              <td style={{ width: "10%" }}>{acc.severity}</td>
              <td style={{ width: "10%" }}>{acc.location}</td>
              <td style={{ width: "10%" }}>{acc.patient ? acc.patient.name : "—"}</td>
            </tr>
          ))}
        </tbody>
      </Table>
    </div>
  );
};

export default Accident;
