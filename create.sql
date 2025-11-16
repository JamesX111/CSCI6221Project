PRAGMA foreign_keys = OFF;

-- Drop existing tables
DROP TABLE IF EXISTS patient;
DROP TABLE IF EXISTS admission;
DROP TABLE IF EXISTS bed_occupancy;
DROP TABLE IF EXISTS staff_schedule;

-- Patient Table
CREATE TABLE patient (
    id INTEGER PRIMARY KEY,
    firstname TEXT,
    lastname TEXT,
    gender TEXT,
    age INTEGER,
    contact_number TEXT
);

-- Admission Table
CREATE TABLE admission (
    id INTEGER PRIMARY KEY,
    patient_id INTEGER NOT NULL,
    bed_id INTEGER NOT NULL,
    admission_date DATETIME,
    discharge_date DATETIME,
    diagnosis TEXT,
    FOREIGN KEY (patient_id) REFERENCES patient(id)
);

-- Bed Occupancy Table
CREATE TABLE bed_occupancy (
    bed_id INTEGER PRIMARY KEY,
    ward TEXT,
    status TEXT,
    last_updated DATETIME
);

-- Staff Schedule Table
CREATE TABLE staff_schedule (
    staff_id INTEGER PRIMARY KEY,
    staff_name TEXT,
    role TEXT,
    shift_start DATETIME,
    shift_end DATETIME
);

PRAGMA foreign_keys = ON;
