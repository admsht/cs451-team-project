-- Function to generate room occupancy report
CREATE OR REPLACE FUNCTION get_occupancy_report
RETURN SYS_REFCURSOR AS
    result SYS_REFCURSOR;
BEGIN
    OPEN result FOR
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
            
    RETURN result;
END get_occupancy_report;
/

-- Procedure to display occupancy report
CREATE OR REPLACE PROCEDURE display_occupancy_report(
    admin_id IN NUMBER,
    message OUT VARCHAR2
) AS
    admin_exists NUMBER;
    report SYS_REFCURSOR;
    room_number NUMBER;
    room_type VARCHAR2(100);
    facility VARCHAR2(100);
    availability VARCHAR2(20);
    total_bookings NUMBER;
    latest_booking DATE;
BEGIN
    -- Check if admin exists
    SELECT COUNT(*) INTO admin_exists FROM Admin WHERE adminID = admin_id;
    
    IF admin_exists = 0 THEN
        message := 'Error: Admin ID does not exist';
        RETURN;
    END IF;
    
    report := get_occupancy_report();
    
    message := 'Room Occupancy Report:' || CHR(10);
    
    LOOP
        FETCH report INTO room_number, room_type, facility, 
                           availability, total_bookings, latest_booking;
        EXIT WHEN report%NOTFOUND;
        
        message := message || 'Room: ' || room_number || 
                     ', Type: ' || room_type ||
                     ', Status: ' || availability || 
                     ', Total Bookings: ' || total_bookings || CHR(10);
    END LOOP;
    
    CLOSE report;
    
EXCEPTION
    WHEN OTHERS THEN
        IF report%ISOPEN THEN
            CLOSE report;
        END IF;
        message := 'Error: ' || SQLERRM;
END display_occupancy_report;
/