-- RoomBookingSystem

-- Student Table
CREATE TABLE Student (
    studentID INT PRIMARY KEY,
    firstName VARCHAR(50) NOT NULL,
    lastName VARCHAR(50) NOT NULL,
    sEmail VARCHAR(100) UNIQUE NOT NULL,
    sPassword VARCHAR(100) NOT NULL
);

-- StudentPhoneNumbers Table
CREATE TABLE StudentPhoneNumbers (
    studentID INT,
    phoneNumber VARCHAR(20),
    PRIMARY KEY (studentID, phoneNumber),
    FOREIGN KEY (studentID) REFERENCES Student(studentID) ON DELETE CASCADE
);

-- Room Table
CREATE TABLE Room (
    roomNumber INT PRIMARY KEY,
    type VARCHAR(100),
    facility VARCHAR(100),
    roomAvailability BOOLEAN 
);

-- RepairRequest Table
CREATE TABLE RepairRequest (
    requestID INT PRIMARY KEY,
    studentID INT,
    roomNumber INT,
    description CLOB,
    repairStatus VARCHAR(25),
    FOREIGN KEY (studentID) REFERENCES Student(studentID) ON DELETE CASCADE,
    FOREIGN KEY (roomNumber) REFERENCES Room(roomNumber) ON DELETE CASCADE
);

-- Admin Table
CREATE TABLE Admin (
    adminID INT PRIMARY KEY,
    aEmail VARCHAR(100) UNIQUE NOT NULL,
    aPassword VARCHAR(100) NOT NULL
);

-- Booking Table
CREATE TABLE Booking (
    bookingID INT PRIMARY KEY,
    studentID INT,
    roomNumber INT,
    status VARCHAR(25) CHECK (status IN ('Pending', 'Confirmed', 'Cancelled')),
    bookingDate DATE NOT NULL,
    FOREIGN KEY (studentID) REFERENCES Student(studentID) ON DELETE CASCADE,
    FOREIGN KEY (roomNumber) REFERENCES Room(roomNumber) ON DELETE CASCADE
);




