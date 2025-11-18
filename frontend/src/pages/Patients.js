import React, { useEffect, useState } from 'react';
import { Table, Form } from 'react-bootstrap';

const Patients = () => {
  const [patients, setPatients] = useState([]);
  const [search, setSearch] = useState("");

  useEffect(() => {
    fetch('http://127.0.0.1:5000/api/get_patients')
      .then(res => {
        if (!res.ok) throw new Error(`HTTP error! status: ${res.status}`);
        return res.json();
      })
      .then(data => setPatients(data))
      .catch(err => console.error("Error fetching patients:", err));
  }, []);

  // Filter patients by name (case-insensitive)
  const filteredPatients = patients.filter(p =>
    p.name.toLowerCase().includes(search.toLowerCase())
  );

  return (
    <div className="container">
      <h2>Patient List</h2>

      {/* 🔍 Search Bar */}
      <Form.Group className="mb-3" controlId="searchBar">
        <Form.Label><strong>Search by Name:</strong></Form.Label>
        <Form.Control
          type="text"
          placeholder="Enter patient name..."
          value={search}
          onChange={(e) => setSearch(e.target.value)}
        />
      </Form.Group>

      <Table striped bordered hover>
        <thead>
          <tr>
            <th>ID</th><th>Name</th><th>Email</th><th>Phone</th>
            <th>Gender</th><th>Address</th><th>Doctor</th>
          </tr>
        </thead>
        <tbody>
          {filteredPatients.length === 0 ? (
            <tr>
              <td colSpan="7" style={{ textAlign: "center" }}>
                No patients found.
              </td>
            </tr>
          ) : (
            filteredPatients.map(p => (
              <tr key={p.id}>
                <td>{p.id}</td>
                <td>{p.name}</td>
                <td>{p.email}</td>
                <td>{p.phone}</td>
                <td>{p.gender}</td>
                <td>{p.address}</td>
                <td>{p.doctor ? p.doctor.name : '—'}</td>
              </tr>
            ))
          )}
        </tbody>
      </Table>
    </div>
  );
};

export default Patients;
