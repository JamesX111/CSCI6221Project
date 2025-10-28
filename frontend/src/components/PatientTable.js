import React from 'react';

const PatientTable = ({ patients }) => {
  if (!patients || patients.length === 0) {
    return <p>No patients found.</p>;
  }

  return (
    <table
      border="1"
      cellPadding="8"
      cellSpacing="0"
      style={{
        borderCollapse: 'collapse',
        width: '100%',
        marginTop: '20px',
        textAlign: 'left',
      }}
    >
      <thead style={{ backgroundColor: '#f2f2f2' }}>
        <tr>
          <th>ID</th>
          <th>Name</th>
          <th>Email</th>
          <th>Phone</th>
          <th>Gender</th>
          <th>Date of Birth</th>
          <th>Address</th>
          <th>Doctor</th>
        </tr>
      </thead>
      <tbody>
        {patients.map((p) => (
          <tr key={p.id}>
            <td>{p.id}</td>
            <td>{p.name}</td>
            <td>{p.email}</td>
            <td>{p.phone}</td>
            <td>{p.gender}</td>
            <td>{p.date_of_birth || 'N/A'}</td>
            <td>{p.address || 'N/A'}</td>
            <td>{p.doctor ? p.doctor.name : '—'}</td>
          </tr>
        ))}
      </tbody>
    </table>
  );
};

export default PatientTable;
