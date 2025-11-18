import React, { useEffect, useState } from 'react';
import { Table, Button, Form } from 'react-bootstrap';
import { Link } from 'react-router-dom';
import './Events.css';

const Events = () => {
  const [events, setEvents] = useState([]);
  const [statusFilter, setStatusFilter] = useState('all');

  useEffect(() => {
    fetch('http://127.0.0.1:5000/api/get_events', { method: 'POST' })
      .then(res => res.json())
      .then(data => setEvents(data))
      .catch(err => console.error(err));
  }, []);

  // Filter events based on selected status
  const filteredEvents = statusFilter === 'all'
    ? events
    : events.filter(e => e.status === statusFilter);

  return (
    <div className="events-page">
      <div className="events-header">
        <h2 className="events-title">Events</h2>
        <Link to="/create-event">
          <Button className="add-event-btn">Add Event</Button>
        </Link>
      </div>

      {/* Status Dropdown */}
      <Form.Group className="mb-3" controlId="statusFilter">
        <Form.Label>Filter by Status</Form.Label>
        <Form.Control
          as="select"
          value={statusFilter}
          onChange={(e) => setStatusFilter(e.target.value)}
        >
          <option value="all">All</option>
          <option value="Completed">Completed</option>
          <option value="Cancelled">Cancelled</option>
          <option value="Scheduled">Scheduled</option>
          <option value="No-Show">No-Show</option>
        </Form.Control>
      </Form.Group>

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
          {filteredEvents.map(e => (
            <tr key={e.id}>
              <td>{e.id}</td>
              <td>{e.type}</td>
              <td>{e.description}</td>
              <td>{e.scheduled}</td>
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
