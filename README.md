# Hospital Management & Real-Time Operations Simulation System

## 1. Introduction
This README provides complete documentation for the Hospital Management and Real-Time Emergency Operations Simulation System. It includes architectural details, installation instructions, API documentation, workflow descriptions, and usage guidelines.

## 2. System Architecture
### 2.1 Frontend (React.js)
Features:
- Live Simulation List and Detail Pages
- Event Acceptance Workflow
- Resource Monitoring (Beds, Nurses, Doctors, Helpers, Departments)
- Appointments Interface
- Patient Dashboard

### 2.2 Backend (Flask + Socket.IO)
Contains:
- Application Factory (app.py)
- Blueprints for API routing
- Real-time event simulation engine (live_simulation.py)
- Resource allocation engine (resource_optimizer.py)
- Patient creation utilities
- SQLite database integration

### 2.3 Database (SQLite)
Primary tables include:
- patients
- nurse
- helpers
- doctor
- hospital
- bed
- bedrecords
- department
- appointment
- accepted_events

## 3. Key System Features
### 3.1 Real-Time Accident Simulation
A background thread randomly generates accident events:
- Includes event type, location, severity
- Predicts patient inflow using ML forecast model
- Simulates temporary resource allocation

### 3.2 Accepting an Event
When a hospital staff member accepts an event:
- Real patients are inserted into the database
- Real bed assignments are created
- A nurse and helper are assigned
- Changes are saved to the `accepted_events` table
- Frontend is updated via WebSocket

### 3.3 Resource Dashboard
Provides real-time dashboards for:
- Beds and occupancy
- Nurses
- Doctors
- Helpers
- Departments

### 3.4 Forecasting Module
The system includes:
- 7-day forecast endpoint
- Flexible horizon forecast endpoint with AI summary
- ML-based admission prediction

## 4. Installation and Setup

### 4.1 Backend Setup
```
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python run.py
```

### 4.2 Frontend Setup
```
cd frontend
npm install
npm start
```

## 5. Running the System
1. Start backend using `python run.py`
2. Start frontend using `npm start`
3. Visit: `http://localhost:3000`
4. Wait for first live event to generate
5. View event details, accept events, and observe real database changes

## 6. Event Workflow
### Step 1 — Simulation Generates Event
Event includes:
- ID
- Type
- Severity
- Location
- Predicted incoming patients
- Temporary simulated allocations

### Step 2 — Staff Views Event
Displayed on:
- LiveSimulationList.js
- LiveSimulationDetail.js

### Step 3 — Accept Event
Upon acceptance:
- Real patients are inserted into database
- Permanent bed assignments created
- Nurse and helper assigned deterministically
- Event is inserted into `accepted_events`
- ACTIVE_EVENTS updated
- Frontend updated in real-time

## 7. API Reference

### Live Simulation
| Endpoint | Method | Description |
|---------|--------|-------------|
| `/api/live-events` | GET | Returns all active simulated events |
| `/api/accept_event` | POST | Accepts an event and allocates resources |

### Hospital Resources
| Endpoint | Method | Description |
|---------|--------|-------------|
| `/api/get_bedding` | GET | Bed status and occupancy |
| `/api/get_nurses` | GET | List of nurses |
| `/api/get_helpers` | GET | List of helpers |
| `/api/get_doctors_list` | GET | Doctor list |
| `/api/get_departments` | GET | Departments |

### Appointments
| Endpoint | Method | Description |
|---------|--------|-------------|
| `/api/get_events` | GET/POST | Appointment + patient + doctor data |

### Patients
| Endpoint | Method | Description |
|---------|--------|-------------|
| `/api/get_patients` | GET | Patient list with filtering |

### Forecasting
| Endpoint | Method | Description |
| `/api/forecast` | GET | 7-day numerical forecast |
| `/api/forecast_summary` | GET | Forecast + AI narrative summary |

## 8. Troubleshooting
### SQLite “database is locked”
Caused by write contention. System now uses:
- Short transactions
- Timeout-enabled connections
- No writes during simulation except acceptance

### Event data not updating
Ensure:
- Backend running with Socket.IO
- Frontend connected via `socket.io-client`

## 9. Future Enhancements
- Workload-based staff assignment
- True staffing schedules
- Real database (PostgreSQL)
- Ambulance routing optimization
- Multi-hospital simulation environment

## 10. Conclusion
This system fully integrates:
- Hospital resource management
- Real-time emergency simulation
- Machine learning forecasting
- Interactive dashboards
- Automated staffing and bed allocation

It is suitable for academic evaluation, demonstrations, and foundational research in real-time hospital operations.
