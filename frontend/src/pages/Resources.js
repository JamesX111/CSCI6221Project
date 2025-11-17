import React, { useEffect, useState } from 'react';
import { Table } from 'react-bootstrap';
import { useNavigate } from 'react-router-dom';

const Resources = () => {
  const [doctors, setDoctors] = useState([]);
  const [wards, setWards] = useState([]);
  const [nurses, setNurses] = useState([]);
  const [helpers, setHelpers] = useState([]);
  const navigate = useNavigate();

  useEffect(() => {
    // Fetch Doctors
    fetch('http://127.0.0.1:5000/api/doctors/get_all', { method: 'POST' })
      .then(res => res.json())
      .then(data => setDoctors(data))
      .catch(err => console.error(err));

    // Fetch Wards
    fetch('http://127.0.0.1:5000/api/wards/get_all', { method: 'POST' })
      .then(res => res.json())
      .then(data => setWards(data))
      .catch(err => console.error(err));

    // Fetch Nurses
    fetch('http://127.0.0.1:5000/api/nurses/get_all', { method: 'POST' })
      .then(res => res.json())
      .then(data => setNurses(data))
      .catch(err => console.error(err));

    // Fetch Helpers
    fetch('http://127.0.0.1:5000/api/helpers/get_all', { method: 'POST' })
      .then(res => res.json())
      .then(data => setHelpers(data))
      .catch(err => console.error(err));
  }, []);

  const tableContainerStyle = {
    maxHeight: '400px', // roughly 10 rows
    overflowY: 'auto',
    marginBottom: '2rem'
  };

  const tableStyle = {
    borderCollapse: 'separate',
    borderSpacing: '0 8px',
    tableLayout: 'fixed', // evenly distribute columns
    width: '100%',
  };

  const headerStyle = { color: '#0b3d91', marginBottom: '1rem' };

  const rowHoverStyle = {
    cursor: 'pointer',
    transition: 'background-color 0.2s'
  };

  const handleRowHover = (e, hover) => {
    e.currentTarget.style.backgroundColor = hover ? '#f0f6ff' : 'transparent';
  };

  return (
    <div style={{ padding: '2rem' }}>
      {/* Doctors */}
      <h2 style={headerStyle}>Doctors</h2>
      <div style={tableContainerStyle}>
        <Table striped bordered hover style={tableStyle}>
          <thead>
            <tr>
              <th>ID</th>
              <th>First Name</th>
              <th>Last Name</th>
              <th>Gender</th>
              <th>Contact</th>
              <th>Dept Name</th>
              <th>Surgeon Type</th>
              <th>Office No</th>
            </tr>
          </thead>
          <tbody>
            {doctors.map(d => (
              <tr key={d.doct_Id}
                  style={rowHoverStyle}
                  onClick={() => navigate(`/update-doctor/${d.doct_Id}`)}
                  onMouseOver={e => handleRowHover(e, true)}
                  onMouseOut={e => handleRowHover(e, false)}>
                <td>{d.doct_Id}</td>
                <td>{d.FName}</td>
                <td>{d.LName}</td>
                <td>{d.Gender}</td>
                <td>{d.contact_No || '—'}</td>
                <td>{d.dept_Name || '—'}</td>
                <td>{d.surgeon_Type || '—'}</td>
                <td>{d.office_No || '—'}</td>
              </tr>
            ))}
          </tbody>
        </Table>
      </div>

      {/* Wards */}
      <h2 style={headerStyle}>Wards</h2>
      <div style={tableContainerStyle}>
        <Table striped bordered hover style={tableStyle}>
          <thead>
            <tr>
              <th>Ward No</th>
              <th>Ward Name</th>
              <th>Dept Id</th>
              <th>Dept Name</th>
            </tr>
          </thead>
          <tbody>
            {wards.map(w => (
              <tr key={w.ward_No}
                  style={rowHoverStyle}
                  onClick={() => navigate(`/update-ward/${w.ward_No}`)}
                  onMouseOver={e => handleRowHover(e, true)}
                  onMouseOut={e => handleRowHover(e, false)}>
                <td>{w.ward_No}</td>
                <td>{w.ward_Name}</td>
                <td>{w.dept_Id}</td>
                <td>{w.dept_Name || '—'}</td>
              </tr>
            ))}
          </tbody>
        </Table>
      </div>

      {/* Nurses */}
      <h2 style={headerStyle}>Nurses</h2>
      <div style={tableContainerStyle}>
        <Table striped bordered hover style={tableStyle}>
          <thead>
            <tr>
              <th>ID</th>
              <th>First Name</th>
              <th>Last Name</th>
              <th>Gender</th>
              <th>Contact</th>
              <th>Dept Id</th>
            </tr>
          </thead>
          <tbody>
            {nurses.map(n => (
              <tr key={n.nurse_Id}
                  style={rowHoverStyle}
                  onClick={() => navigate(`/update-nurse/${n.nurse_Id}`)}
                  onMouseOver={e => handleRowHover(e, true)}
                  onMouseOut={e => handleRowHover(e, false)}>
                <td>{n.nurse_Id}</td>
                <td>{n.FName}</td>
                <td>{n.LName}</td>
                <td>{n.Gender}</td>
                <td>{n.conatct_No || '—'}</td>
                <td>{n.dept_Id}</td>
              </tr>
            ))}
          </tbody>
        </Table>
      </div>

      {/* Helpers */}
      <h2 style={headerStyle}>Helpers</h2>
      <div style={tableContainerStyle}>
        <Table striped bordered hover style={tableStyle}>
          <thead>
            <tr>
              <th>ID</th>
              <th>First Name</th>
              <th>Last Name</th>
              <th>Gender</th>
              <th>Contact</th>
              <th>Dept Id</th>
              <th>Dept Name</th>
            </tr>
          </thead>
          <tbody>
            {helpers.map(h => (
              <tr key={h.helper_Id}
                  style={rowHoverStyle}
                  onClick={() => navigate(`/update-helper/${h.helper_Id}`)}
                  onMouseOver={e => handleRowHover(e, true)}
                  onMouseOut={e => handleRowHover(e, false)}>
                <td>{h.helper_Id}</td>
                <td>{h.FName}</td>
                <td>{h.LName}</td>
                <td>{h.Gender}</td>
                <td>{h.contact_No || '—'}</td>
                <td>{h.dept_Id}</td>
                <td>{h.dept_Name || '—'}</td>
              </tr>
            ))}
          </tbody>
        </Table>
      </div>
    </div>
  );
};

export default Resources;
