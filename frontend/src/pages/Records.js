import React, { useEffect, useState } from 'react';
import { Table } from 'react-bootstrap';
import { useNavigate } from 'react-router-dom';

const Events = () => {
  const [bedRecords, setBedRecords] = useState([]);
  const [roomRecords, setRoomRecords] = useState([]);
  const [surgeryRecords, setSurgeryRecords] = useState([]);
  const navigate = useNavigate();

  useEffect(() => {
    // Fetch Bed Records
    fetch('http://127.0.0.1:5000/api/bed_records/get_all', { method: 'POST' })
      .then(res => res.json())
      .then(data => setBedRecords(data))
      .catch(err => console.error(err));

    // Fetch Room Records
    fetch('http://127.0.0.1:5000/api/room_records/get_all', { method: 'POST' })
      .then(res => res.json())
      .then(data => setRoomRecords(data))
      .catch(err => console.error(err));

    // Fetch Surgery Records
    fetch('http://127.0.0.1:5000/api/surgeries/get_all', { method: 'POST' })
      .then(res => res.json())
      .then(data => setSurgeryRecords(data))
      .catch(err => console.error(err));
  }, []);

  const tableContainerStyle = {
    maxHeight: '400px', // ~10 rows
    overflowY: 'auto',
    marginBottom: '2rem'
  };

  const tableStyle = {
    tableLayout: 'fixed',
    width: '100%'
  };

  const headerStyle = { color: '#0b3d91', marginBottom: '1rem' };
  const rowHoverStyle = { cursor: 'pointer', transition: 'background-color 0.2s' };
  const handleRowHover = (e, hover) => {
    e.currentTarget.style.backgroundColor = hover ? '#f0f6ff' : 'transparent';
  };

  return (
    <div style={{ padding: '2rem' }}>
      {/* Bed Records */}
      <h2 style={headerStyle}>Bed Records</h2>
      <div style={tableContainerStyle}>
        <Table striped bordered hover style={tableStyle}>
          <thead>
            <tr>
              <th>Admission ID</th>
              <th>Bed No</th>
              <th>Patient</th>
              <th>Nurse</th>
              <th>Helper</th>
              <th>Admission Date</th>
              <th>Discharge Date</th>
              <th>Amount</th>
              <th>Payment Mode</th>
            </tr>
          </thead>
          <tbody>
            {bedRecords.map(r => (
              <tr key={r.admission_Id}
                  style={rowHoverStyle}
                  onClick={() => navigate(`/update-bed-record/${r.admission_Id}`)}
                  onMouseOver={e => handleRowHover(e, true)}
                  onMouseOut={e => handleRowHover(e, false)}>
                <td>{r.admission_Id}</td>
                <td>{r.bed_No}</td>
                <td>{r.patient_Name || '—'}</td>
                <td>{r.nurse_Name || '—'}</td>
                <td>{r.helper_Name || '—'}</td>
                <td>{r.admission_Date}</td>
                <td>{r.discharge_Date || '—'}</td>
                <td>{r.amount || '—'}</td>
                <td>{r.mode_of_payment || '—'}</td>
              </tr>
            ))}
          </tbody>
        </Table>
      </div>

      {/* Room Records */}
      <h2 style={headerStyle}>Room Records</h2>
      <div style={tableContainerStyle}>
        <Table striped bordered hover style={tableStyle}>
          <thead>
            <tr>
              <th>Admission ID</th>
              <th>Room No</th>
              <th>Patient</th>
              <th>Nurse</th>
              <th>Helper</th>
              <th>Admission Date</th>
              <th>Discharge Date</th>
              <th>Amount</th>
              <th>Payment Mode</th>
            </tr>
          </thead>
          <tbody>
            {roomRecords.map(r => (
              <tr key={r.admission_ID}
                  style={rowHoverStyle}
                  onClick={() => navigate(`/update-room-record/${r.admission_ID}`)}
                  onMouseOver={e => handleRowHover(e, true)}
                  onMouseOut={e => handleRowHover(e, false)}>
                <td>{r.admission_ID}</td>
                <td>{r.room_no}</td>
                <td>{r.patient_Name || '—'}</td>
                <td>{r.nurse_Name || '—'}</td>
                <td>{r.helper_Name || '—'}</td>
                <td>{r.admission_Date}</td>
                <td>{r.discharge_Date || '—'}</td>
                <td>{r.amount || '—'}</td>
                <td>{r.mode_of_payment || '—'}</td>
              </tr>
            ))}
          </tbody>
        </Table>
      </div>

      {/* Surgery Records */}
      <h2 style={headerStyle}>Surgery Records</h2>
      <div style={tableContainerStyle}>
        <Table striped bordered hover style={tableStyle}>
          <thead>
            <tr>
              <th>Surgery ID</th>
              <th>Patient</th>
              <th>Surgeon</th>
              <th>Surgery Type</th>
              <th>Date</th>
              <th>Start Time</th>
              <th>End Time</th>
              <th>Room No</th>
              <th>Nurse</th>
              <th>Helper</th>
              <th>Notes</th>
            </tr>
          </thead>
          <tbody>
            {surgeryRecords.map(s => (
              <tr key={s.surgery_Id}
                  style={rowHoverStyle}
                  onClick={() => navigate(`/update-surgery/${s.surgery_Id}`)}
                  onMouseOver={e => handleRowHover(e, true)}
                  onMouseOut={e => handleRowHover(e, false)}>
                <td>{s.surgery_Id}</td>
                <td>{s.patient_Name || '—'}</td>
                <td>{s.surgeon_Name || '—'}</td>
                <td>{s.surgery_Type}</td>
                <td>{s.surgery_Date}</td>
                <td>{s.start_Time}</td>
                <td>{s.end_Time}</td>
                <td>{s.room_no || '—'}</td>
                <td>{s.nurse_Name || '—'}</td>
                <td>{s.helper_Name || '—'}</td>
                <td>{s.notes || '—'}</td>
              </tr>
            ))}
          </tbody>
        </Table>
      </div>
    </div>
  );
};

export default Events;
