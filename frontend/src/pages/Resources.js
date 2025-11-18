import React, { useEffect, useState } from 'react';
import { Table, ButtonGroup, Button } from 'react-bootstrap';

const Resources = () => {
  const [view, setView] = useState("beds");

  const [beds, setBeds] = useState([]);
  const [departments, setDepartments] = useState([]);
  const [nurses, setNurses] = useState([]);
  const [doctors, setDoctors] = useState([]);
  const [helpers, setHelpers] = useState([]);

  const fetchAll = () => {
    // Beds
    fetch('http://127.0.0.1:5000/api/get_bedding')
      .then(res => res.json())
      .then(data => setBeds(data))
      .catch(console.error);

    // Departments
    fetch('http://127.0.0.1:5000/api/get_departments')
      .then(res => res.json())
      .then(data => setDepartments(data))
      .catch(console.error);

    // Nurses
    fetch('http://127.0.0.1:5000/api/get_nurses')
      .then(res => res.json())
      .then(data => setNurses(data))
      .catch(console.error);

    // Doctors
    fetch('http://127.0.0.1:5000/api/get_doctors_list')
      .then(res => res.json())
      .then(data => setDoctors(data))
      .catch(console.error);

    // Helpers
    fetch('http://127.0.0.1:5000/api/get_helpers')
      .then(res => res.json())
      .then(data => setHelpers(data))
      .catch(console.error);
  };

  useEffect(() => {
    fetchAll();
    const interval = setInterval(fetchAll, 5000); // refresh every 5s
    return () => clearInterval(interval);
  }, []);

  return (
    <div className="container">
      <h2>Hospital Resources</h2>

      {/* TOP NAV BUTTONS */}
      <ButtonGroup className="my-4">
        <Button 
          variant={view === "beds" ? "primary" : "outline-primary"}
          onClick={() => setView("beds")}
        >
          Beds
        </Button>

        <Button 
          variant={view === "departments" ? "primary" : "outline-primary"}
          onClick={() => setView("departments")}
        >
          Departments
        </Button>

        <Button 
          variant={view === "nurses" ? "primary" : "outline-primary"}
          onClick={() => setView("nurses")}
        >
          Nurses
        </Button>

        <Button 
          variant={view === "doctors" ? "primary" : "outline-primary"}
          onClick={() => setView("doctors")}
        >
          Doctors
        </Button>

        <Button 
          variant={view === "helpers" ? "primary" : "outline-primary"}
          onClick={() => setView("helpers")}
        >
          Helpers
        </Button>
      </ButtonGroup>

      {/* ---------------- BEDS ---------------- */}
      {view === "beds" && (
        <>
          <h4>Bed Occupancy</h4>

          <Table striped bordered hover>
            <thead>
              <tr>
                <th>Bed ID</th>
                <th>Ward</th>
                <th>Status</th>
              </tr>
            </thead>

            <tbody>
              {beds.map(b => (
                <tr key={b.bed_id}>
                  <td>{b.bed_id}</td>
                  <td>{b.ward}</td>
                  <td>{b.status}</td>
                </tr>
              ))}
            </tbody>
          </Table>
        </>
      )}

      {/* ---------------- DEPARTMENTS ---------------- */}
      {view === "departments" && (
        <>
          <h4>Departments</h4>
          <Table striped bordered hover>
            <thead>
              <tr>
                <th>ID</th>
                <th>Name</th>
              </tr>
            </thead>
            <tbody>
              {departments.map(d => (
                <tr key={d.id}>
                  <td>{d.id}</td>
                  <td>{d.name}</td>
                </tr>
              ))}
            </tbody>
          </Table>
        </>
      )}

      {/* ---------------- NURSES ---------------- */}
      {view === "nurses" && (
        <>
          <h4>Nurses</h4>
          <Table striped bordered hover>
            <thead>
              <tr>
                <th>ID</th>
                <th>Name</th>
                <th>Phone</th>
                <th>Gender</th>
              </tr>
            </thead>
            <tbody>
              {nurses.map(n => (
                <tr key={n.id}>
                  <td>{n.id}</td>
                  <td>{n.name}</td>
                  <td>{n.phone}</td>
                  <td>{n.gender}</td>
                </tr>
              ))}
            </tbody>
          </Table>
        </>
      )}

      {/* ---------------- DOCTORS ---------------- */}
      {view === "doctors" && (
        <>
          <h4>Doctors</h4>
          <Table striped bordered hover>
            <thead>
              <tr>
                <th>ID</th>
                <th>Name</th>
                <th>Phone</th>
                <th>Gender</th>
                <th>Specialty</th>
              </tr>
            </thead>
            <tbody>
              {doctors.map(d => (
                <tr key={d.id}>
                  <td>{d.id}</td>
                  <td>{d.name}</td>
                  <td>{d.phone}</td>
                  <td>{d.gender}</td>
                  <td>{d.specialty}</td>
                </tr>
              ))}
            </tbody>
          </Table>
        </>
      )}

      {/* ---------------- HELPERS ---------------- */}
      {view === "helpers" && (
        <>
          <h4>Helpers</h4>
          <Table striped bordered hover>
            <thead>
              <tr>
                <th>ID</th>
                <th>Name</th>
                <th>Phone</th>
                <th>Gender</th>
              </tr>
            </thead>
            <tbody>
              {helpers.map(h => (
                <tr key={h.id}>
                  <td>{h.id}</td>
                  <td>{h.name}</td>
                  <td>{h.phone}</td>
                  <td>{h.gender}</td>
                </tr>
              ))}
            </tbody>
          </Table>
        </>
      )}

    </div>
  );
};

export default Resources;
