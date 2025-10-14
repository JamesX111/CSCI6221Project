SET FOREIGN_KEY_CHECKS=0;

-- Drop existing tables
DROP TABLE IF EXISTS patient;
DROP TABLE IF EXISTS admission;
DROP TABLE IF EXISTS bed_occupancy;
DROP TABLE IF EXISTS staff_schedule;

-- Patient Table
CREATE TABLE patient (
    id INT(8) NOT NULL PRIMARY KEY,
    firstname VARCHAR(50),
    lastname VARCHAR(50),
    gender VARCHAR(10),
    age INT,
    contact_number VARCHAR(20)
);

-- Admission Table
CREATE TABLE admission (
    id INT(8) NOT NULL PRIMARY KEY,
    patient_id INT(8) NOT NULL,
    bed_id INT(8) NOT NULL,
    admission_date DATETIME,
    discharge_date DATETIME,
    diagnosis VARCHAR(255),
    FOREIGN KEY (patient_id) REFERENCES patient(id)
);

-- Bed Occupancy Table
CREATE TABLE bed_occupancy (
    bed_id INT(8) NOT NULL PRIMARY KEY,
    ward VARCHAR(50),
    status VARCHAR(20),
    last_updated DATETIME
);

-- Staff Schedule Table
CREATE TABLE staff_schedule (
    staff_id INT(8) NOT NULL PRIMARY KEY,
    staff_name VARCHAR(100),
    role VARCHAR(50),
    shift_start DATETIME,
    shift_end DATETIME
);
