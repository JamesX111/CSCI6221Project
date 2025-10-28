import React, { useEffect, useState } from 'react';
import { Table } from 'react-bootstrap';

const Patients = () => {
  const [patients, setPatients] = useState([]);

  useEffect(() => {
    fetch('http://127.0.0.1:5000/api/patient/get_all', { method: 'POST' })
      .then(res => res.json())
      .then(data => setPatients(data))
      .catch(err => console.error(err));
  }, []);

  return (
    <div>
      <h2>Patient List</h2>
      <Table striped bordered hover>
        <thead>
          <tr>
            <th>ID</th><th>Name</th><th>Email</th><th>Phone</th>
            <th>Gender</th><th>Address</th><th>Doctor</th>
          </tr>
        </thead>
        <tbody>
          {patients.map(p => (
            <tr key={p.id}>
              <td>{p.id}</td>
              <td>{p.name}</td>
              <td>{p.email}</td>
              <td>{p.phone}</td>
              <td>{p.gender}</td>
              <td>{p.address}</td>
              <td>{p.doctor ? p.doctor.name : '—'}</td>
            </tr>
          ))}
        </tbody>
      </Table>
    </div>
  );
};

export default Patients;
