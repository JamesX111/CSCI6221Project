import React, { useEffect, useState } from 'react';
import { Table, Button } from 'react-bootstrap';
import { useNavigate } from 'react-router-dom';

const Resources = () => {
  const [hospitals, setHospitals] = useState([]);
  const navigate = useNavigate();

  useEffect(() => {
    fetch('http://127.0.0.1:5000/api/get_hospitals', { method: 'POST' })
      .then(res => res.json())
      .then(data => setHospitals(data))
      .catch(err => console.error(err));
  }, []);

  return (
    <div style={{ padding: '2rem' }}>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '1.5rem' }}>
        <h2 style={{ color: '#0b3d91' }}>Hospital Resources</h2>
        <Button
          style={{
            backgroundColor: 'white',
            color: 'black',
            border: '2px solid black',
            borderRadius: '8px',
            fontWeight: 500,
            padding: '6px 16px',
            transition: 'all 0.25s ease-in-out'
          }}
          onMouseOver={(e) => { e.target.style.backgroundColor = 'black'; e.target.style.color = 'white'; }}
          onMouseOut={(e) => { e.target.style.backgroundColor = 'white'; e.target.style.color = 'black'; }}
          onClick={() => navigate('/create-hospital')}
        >
          Create Hospital
        </Button>
      </div>

      <Table striped bordered hover style={{ borderCollapse: 'separate', borderSpacing: '0 8px' }}>
        <thead>
          <tr>
            <th style={{ width: '20%' }}>ID</th>
            <th style={{ width: '20%' }}>Name</th>
            <th style={{ width: '20%' }}>Address</th>
            <th style={{ width: '20%' }}>Number of Doctors</th>
            <th style={{ width: '20%' }}>Number of Beds</th>
          </tr>
        </thead>
        <tbody>
          {hospitals.map(h => (
            <tr
              key={h.id}
              style={{ cursor: 'pointer' }}
              onClick={() => navigate(`/update-hospital/${h.id}`)}
              onMouseOver={(e) => e.currentTarget.style.backgroundColor = '#f0f6ff'}
              onMouseOut={(e) => e.currentTarget.style.backgroundColor = 'transparent'}
            >
              <td style={{ width: '20%' }}>{h.id}</td>
              <td style={{ width: '20%' }}>{h.name}</td>
              <td style={{ width: '20%' }}>{h.address}</td>
              <td style={{ width: '20%' }}>{h.doctors ? h.doctors.length : 0}</td>
              <td style={{ width: '20%' }}>{h.beds ? h.beds.length : 0}</td>
            </tr>
          ))}
        </tbody>
      </Table>
    </div>
  );
};

export default Resources;
