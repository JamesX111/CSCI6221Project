import React, { useEffect, useState } from 'react';
import { Table, Button } from 'react-bootstrap';
import { Link, useNavigate } from 'react-router-dom';
import './Events.css';

const Events = () => {
  const [events, setEvents] = useState([]);
  const navigate = useNavigate();

  useEffect(() => {
    fetch('http://127.0.0.1:5000/api/events/get_all', { method: 'POST' })
      .then(res => res.json())
      .then(data => setEvents(data))
      .catch(err => console.error(err));
  }, []);

  const handleRowClick = (eventId) => {
    navigate(`/update-event/${eventId}`);
  };

  return (
    <div className="events-page">
      <div className="events-header">
        <h2 className="events-title">Events</h2>
        <Link to="/create-event">
          <Button className="add-event-btn">Add Event</Button>
        </Link>
      </div>

      <Table striped bordered hover className="events-table">
        <thead>
          <tr>
            <th>ID</th>
            <th>Type</th>
            <th>Description</th>
            <th>Scheduled</th>
            <th>Status</th>
            <th>Doctor</th>
            <th>Patient</th>
          </tr>
        </thead>
        <tbody>
          {events.map(e => (
            <tr
              key={e.id}
              style={{ cursor: 'pointer' }}
              onClick={() => handleRowClick(e.id)}
            >
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
