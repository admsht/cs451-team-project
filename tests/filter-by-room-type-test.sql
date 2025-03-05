-- Test: Filter by Room Type

-- Arrange: Insert test data for Room records
INSERT INTO Room (roomNumber, type, facility, roomAvailability)
VALUES (101, 'Single', 'WiFi, Air Conditioning', 1);

INSERT INTO Room (roomNumber, type, facility, roomAvailability)
VALUES (102, 'Double', 'WiFi, Heater', 1);

-- Act: Execute the query to filter rooms by type 'Single'
SELECT * FROM Room WHERE type = 'Single';

-- Assert: Manually verify that only the room with roomNumber 101 is returned

ROLLBACK;
