-- Procedure to approve a booking
CREATE OR REPLACE PROCEDURE approve_booking(
    admin_id IN NUMBER,
    booking_id IN NUMBER,
    message OUT VARCHAR2
) AS
    admin_exists NUMBER;
    booking_exists NUMBER;
    current_status VARCHAR2(25);
BEGIN
    -- Check if admin exists
    SELECT COUNT(*) INTO admin_exists FROM Admin WHERE adminID = admin_id;
    
    IF admin_exists = 0 THEN
        message := 'Error: Admin ID does not exist';
        RETURN;
    END IF;
    
    -- Check if booking exists and get current status
    BEGIN
        SELECT status INTO current_status FROM Booking WHERE bookingID = booking_id;
        booking_exists := 1;
    EXCEPTION
        WHEN NO_DATA_FOUND THEN
            booking_exists := 0;
    END;
    
    IF booking_exists = 0 THEN
        message := 'Error: Booking ID does not exist';
        RETURN;
    END IF;
    
    -- Check if booking is already approved
    IF current_status = 'Confirmed' THEN
        message := 'Error: Booking is already confirmed';
        RETURN;
    END IF;
    
    -- Approve booking
    UPDATE Booking 
    SET status = 'Confirmed'
    WHERE bookingID = booking_id;
    
    COMMIT;
    message := 'Booking ' || booking_id || ' has been approved successfully';
    
EXCEPTION
    WHEN OTHERS THEN
        ROLLBACK;
        message := 'Error: ' || SQLERRM;
END approve_booking;
/