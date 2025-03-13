-- Test: Filter by Facilities

-- Arrange: Insert test data for Room records
INSERT INTO Room (roomNumber, type, facility, roomAvailability)
VALUES (101, 'Single', 'WiFi, Air Conditioning', 1);

INSERT INTO Room (roomNumber, type, facility, roomAvailability)
VALUES (102, 'Double', 'Heater, TV', 1);

-- Act: Execute the query to filter rooms that include 'WiFi' in the facility field
SELECT * FROM Room WHERE facility LIKE '%WiFi%';

-- Assert: Manually verify that only room 101 (which includes 'WiFi') is returned

ROLLBACK;
