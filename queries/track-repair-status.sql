-- Query for getting the repair status of a specific students repair
SELECT RepairRequest.requestID, RepairRequest.roomNumber, RepairRequest.description, RepairRequest.repairStatus 
FROM RepairRequest 
WHERE RepairRequest.studentID = 1;  
-- ID will be the students, will display that students repair requests
