import React, { useState } from 'react';
import { Form, Button, Container, Row, Col, Alert } from 'react-bootstrap';
import { useNavigate } from 'react-router-dom';
import './CreateEvent.css';

const CreateEvent = () => {
  const navigate = useNavigate();
  const [formData, setFormData] = useState({
    event_type: '',
    patient_id: '',
    doctor_id: '',
    description: ''
  });

  const [error, setError] = useState('');

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData((prev) => ({ ...prev, [name]: value }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    if (!formData.event_type || !formData.patient_id) {
      setError('Event Type and Patient ID are required.');
      return;
    }

    try {
      const response = await fetch('http://127.0.0.1:5000/api/events/create_event', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(formData)
      });

      if (response.status === 201) {
        navigate('/events');
      } else {
        const data = await response.json();
        setError(data.error || 'Failed to create event.');
      }
    } catch (err) {
      console.error(err);
      setError('Server error. Please try again later.');
    }
  };

  return (
    <Container className="create-event-page">
      <Row className="justify-content-md-center">
        <Col md={8} lg={6}>
          <h2 className="create-event-title">Create Event</h2>

          <Form onSubmit={handleSubmit} className="create-event-form">
            <Form.Group className="mb-4 form-field">
              <Form.Label>Event Type <span className="required">*</span></Form.Label>
              <Form.Control
                type="text"
                name="event_type"
                maxLength="50"
                placeholder="Enter event type"
                value={formData.event_type}
                onChange={handleChange}
                required
              />
            </Form.Group>

            <Form.Group className="mb-4 form-field">
              <Form.Label>Patient ID <span className="required">*</span></Form.Label>
              <Form.Control
                type="number"
                name="patient_id"
                placeholder="Enter patient ID"
                value={formData.patient_id}
                onChange={handleChange}
                required
              />
            </Form.Group>

            <Form.Group className="mb-4 form-field">
              <Form.Label>Doctor ID</Form.Label>
              <Form.Control
                type="number"
                name="doctor_id"
                placeholder="Enter doctor ID (optional)"
                value={formData.doctor_id}
                onChange={handleChange}
              />
            </Form.Group>

            {/* Description textarea aligned with other fields */}
            <Form.Group className="mb-4 form-field">
              <Form.Label>Description</Form.Label>
              <Form.Control
                as="textarea"
                name="description"
                placeholder="Enter description (optional)"
                rows={5}
                value={formData.description}
                onChange={handleChange}
              />
            </Form.Group>
          </Form>

          {/* Error message */}
          {error && <Alert variant="danger" className="text-center">{error}</Alert>}

          {/* Centered Create button */}
          <div className="create-event-btn-wrapper">
            <Button type="submit" className="create-event-btn" onClick={handleSubmit}>
              Create Event
            </Button>
          </div>

        </Col>
      </Row>
    </Container>
  );
};

export default CreateEvent;
