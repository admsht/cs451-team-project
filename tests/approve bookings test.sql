-- 1. Insert test data
INSERT INTO Room (roomNumber, type, facility, roomAvailability)
VALUES (202, 'Double', 'Wi-Fi', 1);

-- 2. Create a pending booking
DECLARE
    next_id NUMBER;
BEGIN
    SELECT NVL(MAX(bookingID), 0) + 1 INTO next_id FROM Booking;
    
    INSERT INTO Booking (bookingID, studentID, roomNumber, status, bookingDate)
    VALUES (next_id, 101, 202, 'Pending', SYSDATE);
END;
/

-- 3. Get booking ID for testing
SELECT MAX(bookingID) AS pending_booking_id FROM Booking WHERE status = 'Pending';

-- 4. Test approve_booking procedure (replace X with actual booking ID from above query)
DECLARE
    message VARCHAR2(200);
BEGIN
    approve_booking(1, X, message);
END;
/

-- 5. Verify the results
SELECT bookingID, status FROM Booking WHERE bookingID = X;