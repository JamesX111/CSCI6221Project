import React from 'react';
import { useNavigate } from 'react-router-dom';
import { Button } from 'react-bootstrap';

const Home = () => {
  const navigate = useNavigate();

  return (
    <div className="text-center mt-5">
      <h1>🏥 Hospital Management System</h1>
      <p className="text-muted">Choose a section below:</p>

      <div className="d-flex justify-content-center gap-3 mt-4">
        <Button variant="primary" onClick={() => navigate('/patients')}>
          View Patients
        </Button>
        <Button variant="success" onClick={() => navigate('/events')}>
          View Events
        </Button>
        <Button variant="info" onClick={() => navigate('/resources')}>
          Hospital Resources
        </Button>
      </div>
    </div>
  );
};

export default Home;
