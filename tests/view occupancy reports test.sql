-- 1. Insert test data
INSERT INTO Room (roomNumber, type, facility, roomAvailability)
VALUES (203, 'Suite', 'Kitchen, Wi-Fi', 1);

INSERT INTO Room (roomNumber, type, facility, roomAvailability)
VALUES (204, 'Single', 'Shared Bathroom', 0);

-- 2. Create some bookings
DECLARE
    next_id NUMBER;
BEGIN
    SELECT NVL(MAX(bookingID), 0) + 1 INTO next_id FROM Booking;
    
    INSERT INTO Booking (bookingID, studentID, roomNumber, status, bookingDate)
    VALUES (next_id, 101, 203, 'Confirmed', SYSDATE - 5);
    
    INSERT INTO Booking (bookingID, studentID, roomNumber, status, bookingDate)
    VALUES (next_id + 1, 101, 204, 'Confirmed', SYSDATE - 10);
END;
/

-- Method 1: Test using the stored procedure
DECLARE
    message CLOB;
BEGIN
    display_occupancy_report(1, message);
END;
/

-- Method 2: Run the direct query
SELECT 
    r.roomNumber,
    r.type AS room_type,
    r.facility,
    CASE 
        WHEN r.roomAvailability = 1 THEN 'Available'
        ELSE 'Occupied'
    END AS availability_status,
    (SELECT COUNT(*) 
     FROM Booking b 
     WHERE b.roomNumber = r.roomNumber 
     AND b.status = 'Confirmed') AS total_bookings,
    (SELECT MAX(b.bookingDate) 
     FROM Booking b 
     WHERE b.roomNumber = r.roomNumber 
     AND b.status = 'Confirmed') AS latest_booking_date
FROM 
    Room r
ORDER BY 
    r.roomNumber;