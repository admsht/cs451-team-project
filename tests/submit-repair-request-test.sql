-- need a student and room first
INSERT INTO Student (studentID, firstName, lastName, sEmail, sPassword) VALUES (1, 'Joshua', 'Allard', 'joshua.allard@wsu.edu', 'password');

-- insert room
INSERT INTO Room (roomNumber, type, facility, roomAvailability) VALUES (101, 'Single', 'WiFi, AC', 'Not Available');

-- Query for subbmiting repair request 
INSERT INTO RepairRequest (requestID, studentID, roomNumber, description, repairStatus) VALUES (1, 1, 101, 'Leaking sink', 'Pending');

-- get all reapir requests, should show the repair request entered
SELECT * FROM RepairRequest;
