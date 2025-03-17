-- need a student, room, and repair request first
INSERT INTO Student (studentID, firstName, lastName, sEmail, sPassword) VALUES (1, 'Joshua', 'Allard', 'joshua.allard@wsu.edu', 'password');

-- insert room
INSERT INTO Room (roomNumber, type, facility, roomAvailability) VALUES (101, 'Single', 'WiFi, AC', 'Not Available');

-- Query for subbmiting repair request 
INSERT INTO RepairRequest (requestID, studentID, roomNumber, description, repairStatus) VALUES (1, 1, 101, 'Leaking sink', 'Pending');


-- Query for getting the repair status of a specific students repair
SELECT RepairRequest.requestID, RepairRequest.roomNumber, RepairRequest.description, RepairRequest.repairStatus 
FROM RepairRequest 
WHERE RepairRequest.studentID = 1;  
-- ID will be the students, will display that students repair requests