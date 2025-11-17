import React, { useEffect, useState } from 'react';
import { Table } from 'react-bootstrap';

const Resources = () => {
  const [hospitals, setHospitals] = useState([]);
  const [beds, setBeds] = useState([]);

  useEffect(() => {
    fetch('http://127.0.0.1:5000/api/get_hospitals', { method: 'POST' })
      .then(res => res.json())
      .then(data => setHospitals(data))
      .catch(err => console.error(err));

    fetch('http://127.0.0.1:5000/api/get_bedding', { method: 'POST' })
      .then(res => res.json())
      .then(data => setBeds([data]))
      .catch(err => console.error(err));
  }, []);

  return (
    <div className="container">
      <h2>Hospital Resources</h2>

      <h4 className="mt-5">Bed Occupancy</h4>
      {beds.length > 0 ? (
        <Table striped bordered hover>
          <thead>
            <tr><th>Bed ID</th><th>Ward</th><th>Status</th><th>Last Updated</th></tr>
          </thead>
          <tbody>
            {beds.map(b => (
              <tr key={b.bed_id}>
                <td>{b.bed_id}</td>
                <td>{b.ward}</td>
                <td>{b.status}</td>
                <td>{b.last_updated}</td>
              </tr>
            ))}
          </tbody>
        </Table>
      ) : (
        <p>No bed occupancy data found.</p>
      )}
      <h4 className="mt-4">Hospitals</h4>
      <Table striped bordered hover>
        <thead>
          <tr>
            <th>ID</th><th>Name</th><th>Address</th><th>Phone</th>
            <th>Email</th><th>Departments</th>
          </tr>
        </thead>
        <tbody>
          {hospitals.map(h => (
            <tr key={h.id}>
              <td>{h.id}</td>
              <td>{h.name}</td>
              <td>{h.address}</td>
              <td>{h.phone}</td>
              <td>{h.email}</td>
              <td>
                {Object.keys(h.departments)
                  .filter(dep => h.departments[dep])
                  .join(', ') || 'None'}
              </td>
            </tr>
          ))}
        </tbody>
      </Table>

      
    </div>
  );
};

export default Resources;
