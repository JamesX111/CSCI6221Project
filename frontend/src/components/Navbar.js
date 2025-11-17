import React from 'react';
import { Link } from 'react-router-dom';
import { Navbar, Nav, Container } from 'react-bootstrap';
import './Navbar.css';

const NavBar = () => (
  <Navbar
    expand={false}
    style={{
      backgroundColor: '#0d1b3d',
      height: '80px',
      display: 'flex',
      alignItems: 'center',
    }}
  >
    <Container
      fluid
      style={{
        display: 'flex',
        alignItems: 'center',
      }}
    >
      <Navbar.Brand
        as={Link}
        to="/"
        style={{
          color: 'white',
          fontWeight: 'bold',
          fontSize: '1.5rem',
          marginLeft: '20px',
          display: 'flex',
          alignItems: 'center',
        }}
      >
        Hospital Management
      </Navbar.Brand>

      <Nav
        style={{
          display: 'flex',
          alignItems: 'center',
          gap: '30px',
          marginLeft: 'auto',
          marginRight: '40px',
        }}
      >
        <div className="navbar">
          <div className="brand"></div>
          <div>
            <Link to="/">Live Simulation</Link>
            <Link to="/patients">Patients</Link>
            <Link to="/events">Events</Link>
            <Link to="/resources">Resources</Link>
            <Link to="/forecast">Forecast</Link>
          </div>
        </div>
      </Nav>
    </Container>
  </Navbar>
);

export default NavBar;
