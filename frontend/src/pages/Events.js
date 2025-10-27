import React, { useEffect, useState } from 'react';
import { Table } from 'react-bootstrap';

const Events = () => {
  const [events, setEvents] = useState([]);

  useEffect(() => {
    fetch('http://127.0.0.1:5000/api/get_events', { method: 'POST' })
      .then(res => res.json())
      .then(data => setEvents(data))
      .catch(err => console.error(err));
  }, []);

  return (
    <div>
      <h2>Events</h2>
      <Table striped bordered hover>
        <thead>
          <tr>
            <th>ID</th><th>Type</th><th>Description</th>
            <th>Scheduled</th><th>Status</th><th>Doctor</th><th>Patient</th>
          </tr>
        </thead>
        <tbody>
          {events.map(e => (
            <tr key={e.id}>
              <td>{e.id}</td>
              <td>{e.event_type}</td>
              <td>{e.description}</td>
              <td>{e.scheduled_at}</td>
              <td>{e.status}</td>
              <td>{e.doctor ? e.doctor.name : '—'}</td>
              <td>{e.patient ? e.patient.name : '—'}</td>
            </tr>
          ))}
        </tbody>
      </Table>
    </div>
  );
};

export default Events;
