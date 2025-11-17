import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Home from './pages/Home';
import Patients from './pages/Patients';
import Resources from './pages/Resources';
import Navbar from './components/Navbar';
import CreateEvent from './pages/CreateEvent';
import Appointments from './pages/Appointments';
import CreateAccident from './pages/CreateAccident';
import UpdateAccident from './pages/UpdateAccident'; 
import UpdateEvent from './pages/UpdateEvent';
import CreateHospital from './pages/CreateHospital';
import CreateBed from './pages/CreateBed';
import UpdateBed from './pages/UpdateBed';
import CreateDoctor from './pages/CreateDoctor';
import UpdateDoctor from './pages/UpdateDoctor';
import Records from './pages/Records';
import UpdatePatient from './pages/UpdatePatient';
import UpdateWard from './pages/UpdateWard';

function App() {
  const navbarLinks = [
    { path: '/patients', label: 'Patients' },
    { path: '/records', label: 'Records' },
    { path: '/resources', label: 'Resources' },
  ];

  return (
    <Router>
      <Navbar title="Scheduler App" links={navbarLinks} />
      <div className="container mt-4">
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/patients" element={<Patients />} />
          <Route path="/records" element={<Records />} />
          <Route path="/resources" element={<Resources />} />
          <Route path="/create-event" element={<CreateEvent />} />
          <Route path="/appointments" element={<Appointments />} />
          <Route path="/create-accident" element={<CreateAccident />} />
          <Route path="/update-accident/:id" element={<UpdateAccident />} />
          <Route path="/update-event/:eventId" element={<UpdateEvent />} />
          <Route path="/create-hospital" element={<CreateHospital />} />
          <Route path="/create-bed/:hospitalId" element={<CreateBed />} />
          <Route path="/update-bed/:bedId" element={<UpdateBed />} />
          <Route path="/create-doctor/:hospitalId" element={<CreateDoctor />} />
          <Route path="/update-doctor/:doctorId" element={<UpdateDoctor />} />
          <Route path="/update-patient/:patientId" element={<UpdatePatient />} />
          <Route path="/update-ward/:wardNo" element={<UpdateWard />} />

        </Routes>
      </div>
    </Router>
  );
}

export default App;
