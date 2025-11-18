import React, { useEffect, useState } from 'react';
import { Table, Form } from 'react-bootstrap';

const Patients = () => {
  // default to admitted
  const [patients, setPatients] = useState([]);
  const [status, setStatus] = useState("admitted");

  const loadPatients = () => {
    fetch(`http://127.0.0.1:5000/api/get_patients?status=${status}`)
      .then(res => res.json())
      .then(data => setPatients(data))
      .catch(err => console.error("Error:", err));
  };

  useEffect(() => {
    loadPatients();
  }, [status]);

  return (
    <div className="container">
      <h2>Patient List</h2>

      {/* 🔘 Only two options now */}
      <Form.Select
        size="lg"
        style={{ width: "260px", marginBottom: "20px" }}
        value={status}
        onChange={e => setStatus(e.target.value)}
      >
        <option value="admitted">Admitted Patients</option>
        <option value="completed">Completed Patients</option>
      </Form.Select>

      <Table striped bordered hover>
        <thead>
          <tr>
            <th>Name</th>
            <th>Email</th>
            <th>Age</th>
            <th>Phone</th>
            <th>Gender</th>
            <th>Address</th>
            <th>Bed</th>
            <th>Doctor</th>
            <th>Admitted On</th>
            <th>Discharged On</th>
          </tr>
        </thead>
        <tbody>
          {patients.map((p, i) => (
            <tr key={i}>
              <td>{p.name}</td>
              <td>{p.email}</td>
              <td>{p.age || "—"}</td>
              <td>{p.phone}</td>
              <td>{p.gender}</td>
              <td>{p.address}</td>
              <td>{p.bed_number || "—"}</td>
              <td>{p.doctor || "—"}</td>
              <td>{p.admitted_on || "—"}</td>
              <td>{p.discharged_on || "—"}</td>
            </tr>
          ))}
        </tbody>
      </Table>
    </div>
  );
};

export default Patients;
