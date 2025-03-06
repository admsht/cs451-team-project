-- Procedure to assign a room to a student
CREATE OR REPLACE PROCEDURE assign_room(
    admin_id IN NUMBER,
    student_id IN NUMBER,
    room_number IN NUMBER,
    booking_date IN DATE,
    message OUT VARCHAR2
) AS
    room_available NUMBER;
    admin_exists NUMBER;
    student_exists NUMBER;
    booking_id NUMBER;
BEGIN
    -- Check if admin exists
    SELECT COUNT(*) INTO admin_exists FROM Admin WHERE adminID = admin_id;
    
    IF admin_exists = 0 THEN
        message := 'Error: Admin ID does not exist';
        RETURN;
    END IF;
    
    -- Check if student exists
    SELECT COUNT(*) INTO student_exists FROM Student WHERE studentID = student_id;
    
    IF student_exists = 0 THEN
        message := 'Error: Student ID does not exist';
        RETURN;
    END IF;
    
    -- Check if room is available
    SELECT roomAvailability INTO room_available 
    FROM Room WHERE roomNumber = room_number;
    
    IF room_available = 0 THEN
        message := 'Error: Room is not available';
        RETURN;
    END IF;
    
    -- Generate a new booking ID
    SELECT NVL(MAX(bookingID), 0) + 1 INTO booking_id FROM Booking;
    
    -- Create a new booking
    INSERT INTO Booking (bookingID, studentID, roomNumber, status, bookingDate)
    VALUES (booking_id, student_id, room_number, 'Confirmed', booking_date);
    
    -- Update room availability to unavailable
    UPDATE Room SET roomAvailability = 0 WHERE roomNumber = room_number;
    
    COMMIT;
    message := 'Room ' || room_number || ' successfully assigned to student ' || student_id;
    
EXCEPTION
    WHEN OTHERS THEN
        ROLLBACK;
        message := 'Error: ' || SQLERRM;
END assign_room;
/