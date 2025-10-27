import React from 'react';
import { Link } from 'react-router-dom';
import { Navbar, Nav, Container } from 'react-bootstrap';

const NavBar = () => (
  <Navbar bg="dark" variant="dark" expand="lg">
    <Container>
      <Navbar.Brand as={Link} to="/">Hospital Management</Navbar.Brand>
      <Nav className="me-auto">
        <Nav.Link as={Link} to="/">Home</Nav.Link>
        <Nav.Link as={Link} to="/patients">Patients</Nav.Link>
        <Nav.Link as={Link} to="/events">Events</Nav.Link>
        <Nav.Link as={Link} to="/resources">Resources</Nav.Link>
      </Nav>
    </Container>
  </Navbar>
);

export default NavBar;
