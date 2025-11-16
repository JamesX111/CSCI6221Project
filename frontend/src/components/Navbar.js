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
      {/* Left side: brand */}
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

      {/* Right side: nav links */}
      <Nav
        style={{
          display: 'flex',
          alignItems: 'center',
          gap: '30px',
          marginLeft: 'auto', // pushes to the right edge
          marginRight: '40px',
        }}
      >
        <div className="navbar">
          <div className="brand"></div>
          <div>
            <a href="/patients">Patients</a>
            <a href="/events">Events</a>
            <a href="/resources">Resources</a>
            <a href="/forecast">Forecast</a>
          </div>
        </div>
      </Nav>
    </Container>
  </Navbar>
);

export default NavBar;
