-- 1. Insert test data
INSERT INTO Admin (adminID, aEmail, aPassword)
VALUES (1, 'admin@university.edu', 'admin123');

INSERT INTO Student (studentID, firstName, lastName, sEmail, sPassword)
VALUES (101, 'John', 'Smith', 'john.smith@student.edu', 'student123');

INSERT INTO Room (roomNumber, type, facility, roomAvailability)
VALUES (201, 'Single', 'Air Conditioning', 1);

-- 2. Test the assign_room procedure
DECLARE
    message VARCHAR2(200);
BEGIN
    assign_room(1, 101, 201, SYSDATE, message);
END;
/

-- 3. Query to verify results
SELECT roomNumber, roomAvailability FROM Room WHERE roomNumber = 201;
SELECT bookingID, studentID, roomNumber, status FROM Booking WHERE roomNumber = 201;