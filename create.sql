

SET FOREIGN_KEY_CHECKS=0;

DROP TABLE IF EXISTS patient;
DROP TABLE IF EXISTS admission;
DROP TABLE IF EXISTS bed_occupancy;
DROP TABLE IF EXISTS staff_schedule;


CREATE TABLE patient(
    id int(8) NOT NULL,
    firstname varchar(50),
    lastname varchar(50)
)

CREATE TABLE admission(
    id int(8) NOT NULL,
    bed_id int(8) NOT NULL,

)