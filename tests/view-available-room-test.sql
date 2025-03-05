-- Test 2: View Available Rooms

-- Arrange: Insert test data for Room records
INSERT INTO Room (roomNumber, type, facility, roomAvailability)
VALUES (101, 'Single', 'WiFi, Air Conditioning', 1);

INSERT INTO Room (roomNumber, type, facility, roomAvailability)
VALUES (102, 'Double', 'WiFi, Heater', 0);

-- Act: Execute the query to list only available rooms
SELECT * FROM Room WHERE roomAvailability = 1;

-- Assert: Manually verify that only room 101 (with roomAvailability = 1) is returned

ROLLBACK;
