import React, { useEffect, useState } from "react";
import { useNavigate, useParams } from "react-router-dom";
import Table from "react-bootstrap/Table";

const UpdateWard = () => {
  const { wardNo } = useParams();
  const navigate = useNavigate();

  const [wardData, setWardData] = useState({
    ward_No: "",
    ward_Name: "",
    dept_Id: "",
    dept_Name: "",
  });

  const [beds, setBeds] = useState([]);
  const [departments, setDepartments] = useState([]);
  const [error, setError] = useState("");

  // Fetch ward info
  useEffect(() => {
    const fetchWard = async () => {
      try {
        const res = await fetch(
          `http://127.0.0.1:5000/api/wards/get/${wardNo}`,
          { method: "POST" }
        );

        const data = await res.json();

        if (!res.ok) {
          setError(data.error || "Failed to load ward");
        } else {
          setWardData({
            ward_No: data.ward_No,
            ward_Name: data.ward_Name,
            dept_Id: data.dept_Id,
            dept_Name: data.dept_Name,
          });
        }
      } catch (err) {
        setError("Failed to load ward");
        console.error(err);
      }
    };

    fetchWard();
  }, [wardNo]);

  // Fetch departments for dropdown
  useEffect(() => {
    const fetchDepartments = async () => {
      try {
        const res = await fetch("http://127.0.0.1:5000/api/departments/get_all");
        const data = await res.json();
        if (res.ok) setDepartments(data);
      } catch (err) {
        console.error("Failed to load departments");
      }
    };
    fetchDepartments();
  }, []);

  // Fetch beds for ward
  useEffect(() => {
    const fetchBeds = async () => {
      try {
        const res = await fetch(
          `http://127.0.0.1:5000/api/beds/get_by_ward/${wardNo}`
        );
        const data = await res.json();
        if (res.ok) setBeds(data);
      } catch (err) {
        console.error("Failed to load beds");
      }
    };
    fetchBeds();
  }, [wardNo]);

  const handleChange = (e) => {
    const { name, value } = e.target;
    setWardData({ ...wardData, [name]: value });
  };

  const handleUpdate = async () => {
    setError("");

    try {
      const res = await fetch(
        `http://127.0.0.1:5000/api/wards/update/${wardNo}`,
        {
          method: "PUT",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify(wardData),
        }
      );

      const data = await res.json();

      if (!res.ok) setError(data.error || "Update failed");
      else navigate("/resources");
    } catch (err) {
      setError("Failed to update ward");
      console.error(err);
    }
  };

  const handleDelete = async () => {
    if (!window.confirm("Are you sure you want to delete this ward?")) return;

    try {
      const res = await fetch(
        `http://127.0.0.1:5000/api/wards/delete/${wardNo}`,
        { method: "DELETE" }
      );

      const data = await res.json();

      if (!res.ok) setError(data.error || "Delete failed");
      else navigate("/wards");
    } catch (err) {
      setError("Failed to delete ward");
    }
  };

  return (
    <div style={{ maxWidth: "800px", margin: "2rem auto" }}>
      <h2 style={{ color: "#0b3d91", textAlign: "center" }}>
        Update Ward
      </h2>

      {error && <p style={{ color: "red", textAlign: "center" }}>{error}</p>}

      {/* Ward Number (readonly) */}
      <div style={{ marginBottom: "1.5rem" }}>
        <label>Ward Number</label>
        <input
          type="text"
          name="ward_No"
          value={wardData.ward_No}
          readOnly
          style={{ width: "100%", marginTop: "0.5rem", backgroundColor: "#eee" }}
        />
      </div>

      {/* Ward Name */}
      <div style={{ marginBottom: "1.5rem" }}>
        <label>Ward Name</label>
        <input
          type="text"
          name="ward_Name"
          value={wardData.ward_Name}
          onChange={handleChange}
          style={{ width: "100%", marginTop: "0.5rem" }}
        />
      </div>

      {/* Department */}
      <div style={{ marginBottom: "1.5rem" }}>
        <label>Department</label>
        <select
          name="dept_Id"
          value={wardData.dept_Id}
          onChange={handleChange}
          style={{ width: "100%", marginTop: "0.5rem", padding: "6px" }}
        >
          <option value="">Select Department</option>
          {departments.map((d) => (
            <option key={d.dept_Id} value={d.dept_Id}>
              {d.dept_Name}
            </option>
          ))}
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

      {/* ============================= */}
      {/*         BED TABLE             */}
      {/* ============================= */}
      <h3 style={{ marginTop: "3rem", textAlign: "center", color: "#0b3d91" }}>
        Beds in Ward
      </h3>

      <Table
        bordered
        hover
        style={{
          width: "100%",
          tableLayout: "fixed",
          wordWrap: "break-word",
        }}
      >
        <thead style={{ backgroundColor: "#f5f5f5" }}>
          <tr>
            <th style={{ width: "15%" }}>Bed Number</th>
            <th style={{ width: "15%" }}>Ward Number</th>
            <th style={{ width: "20%" }}>Availability</th>
          </tr>
        </thead>

        <tbody>
          {beds.length === 0 ? (
            <tr>
              <td colSpan="3" style={{ textAlign: "center", padding: "12px" }}>
                No beds found.
              </td>
            </tr>
          ) : (
            beds.map((b) => (
              <tr key={b.bed_No}>
                <td style={{ padding: "10px" }}>{b.bed_No}</td>
                <td style={{ padding: "10px" }}>{b.ward_No}</td>
                <td style={{ padding: "10px" }}>
                  {b.available || "Available"}
                </td>
              </tr>
            ))
          )}
        </tbody>
      </Table>
    </div>
  );
};

export default UpdateWard;
