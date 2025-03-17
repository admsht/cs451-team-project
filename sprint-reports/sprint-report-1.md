# Sprint 1 Report 
Video Link: https://drive.google.com/file/d/1LZ4Rbg8qxbhGjlpNBFfukLlSANtcncsT/view?usp=sharing
## What's New (User Facing)
* **Enhanced User Interfaces:**  
  Implemented responsive and user-friendly HTML pages for login, registration, and dashboard functionalities, ensuring seamless navigation and intuitive interactions.
* **Improved Room Filtering:**  
  Introduced SQL functions that let users filter available rooms by facilities, room types, and availability, making it easier for users to find the perfect room based on their needs.
* **Reliable Booking Information:**  
  Developed comprehensive tests for the SQL functions, ensuring that users always receive accurate and up-to-date room information.

## Work Summary (Developer Facing)
Our primary focus during this sprint was to establish the core functionalities that connect the frontend with our underlying database operations. We achieved this by:
* **Implementing Key Components:**  
  Developed foundational HTML pages for authentication (login, registration) and dashboard views, integrating them with backend logic.
* **SQL Query Development:**  
  Created and optimized SQL functions to retrieve filtered data from our Room table based on various parameters such as room type, facilities, and availability.
* **Testing & Quality Assurance:**  
  Crafted and executed test cases for each SQL function to validate our filtering and retrieval logic, ensuring the system behaves as expected.
* **Collaboration & Best Practices:**  
  Worked collaboratively to resolve integration challenges, upheld best practices in coding, and ensured our SQL implementations can be effectively translated and maintained in PostgreSQL.
  

## Completed Issues/User Stories
Here are links to the issues that we completed in this sprint:

 * [Create SQL Tables](https://github.com/users/admsht/projects/2/views/1?pane=issue&itemId=100777174&issue=admsht%7Ccs451-team-project%7C13)
 * [Create login page](https://github.com/users/admsht/projects/2/views/1?pane=issue&itemId=101193157&issue=admsht%7Ccs451-team-project%7C14)
 * [UserStory2: View Available Rooms](https://github.com/users/admsht/projects/2/views/1?pane=issue&itemId=100373595&issue=admsht%7Ccs451-team-project%7C2)
 * [UserStory3: Filter by Room Type](https://github.com/users/admsht/projects/2/views/1?pane=issue&itemId=100373831&issue=admsht%7Ccs451-team-project%7C3)
 * [UserStory4: Filter by Facilities](https://github.com/users/admsht/projects/2/views/1?pane=issue&itemId=100374706&issue=admsht%7Ccs451-team-project%7C4)
 * [UserStory6: Submit Repair Requests](https://github.com/users/admsht/projects/2/views/1?pane=issue&itemId=100374708&issue=admsht%7Ccs451-team-project%7C6)
 * [UserStory7: Track Repair Status](https://github.com/users/admsht/projects/2/views/1?pane=issue&itemId=100374709&issue=admsht%7Ccs451-team-project%7C7)

 
 ## Incomplete Issues/User Stories
Here are links to issues we worked on but did not complete in this sprint:

* [UserStory11: Admin Booking Approval](https://github.com/users/admsht/projects/2/views/1?pane=issue&itemId=100374713&issue=admsht%7Ccs451-team-project%7C11):  
  We did not get to this issue because the admin portal is still under development and we prioritized core user functionalities during this sprint. We will continue in Sprint 2.

* [UserStory10: Admin Room Assignment](https://github.com/users/admsht/projects/2/views/1?pane=issue&itemId=100374712&issue=admsht%7Ccs451-team-project%7C10):  
  We did not get to this issue due to scheduling conflicts and the need to focus on stabilizing the frontend integration. We will continue in Sprint 2.

* [UserStory12: Admin Occupancy Reports](https://github.com/users/admsht/projects/2/views/1?pane=issue&itemId=100374714&issue=admsht%7Ccs451-team-project%7C12):  
  We did not get to this issue because the admin portal is not fully operational; occupancy reports are postponed until the portal framework is complete. We will continue in Sprint 2.

* [UserStory9: Maintenance Update Notifications](https://github.com/users/admsht/projects/2/views/1?pane=issue&itemId=100374711&issue=admsht%7Ccs451-team-project%7C9):  
  We did not implement this feature because the backend scheduling service required for reminders was not ready in time. We will continue in Sprint 2.

* [UserStory8: Booking Deadline Reminders](https://github.com/users/admsht/projects/2/views/1?pane=issue&itemId=100374710&issue=admsht%7Ccs451-team-project%7C8):  
  We did not implement this feature because the backend scheduling service required for reminders was not ready in time. We will continue in Sprint 2.

* [UserStory5: Book Room](https://github.com/users/admsht/projects/2/views/1?pane=issue&itemId=100374707&issue=admsht%7Ccs451-team-project%7C5):  
  We did not fully complete this feature as additional testing is required to meet our reliability standards. We will continue in Sprint 2.

* [UserStory1: Student Profile Registration](https://github.com/users/admsht/projects/2/views/1?pane=issue&itemId=100373345&issue=admsht%7Ccs451-team-project%7C1):  
  We did not fully complete this feature as additional testing is required to meet our reliability standards. We will continue in Sprint 2.


## Code Files for Review
Please review the following code files, which were actively developed during this sprint, for quality:
 * [RoomBookingSystem.py](https://github.com/admsht/cs451-team-project/blob/main/Project/RoomBookingSystem.py)
 * [Dashboard.html](https://github.com/admsht/cs451-team-project/blob/main/Project/dashboard.html)
 * [Layout.html](https://github.com/admsht/cs451-team-project/blob/main/Project/layout.html)
 * [Login.html](https://github.com/admsht/cs451-team-project/blob/main/Project/login.html)
 * [Register.html](https://github.com/admsht/cs451-team-project/blob/main/Project/register.html)
 * [Filter-by-facilities.sql](https://github.com/admsht/cs451-team-project/blob/main/queries/filter-by-facilities.sql)
 * [Filter-by-room-type.sql](https://github.com/admsht/cs451-team-project/blob/main/queries/filter-by-room-type.sql)
 * [View-available-rooms.sql](https://github.com/admsht/cs451-team-project/blob/main/queries/view-available-rooms.sql)
 * [Filter-by-facilities-test.sql](https://github.com/admsht/cs451-team-project/blob/main/tests/filter-by-facilities-test.sql)
 * [Filter-by-room-type-test.sql](https://github.com/admsht/cs451-team-project/blob/main/tests/filter-by-room-type-test.sql)
 * [View-available-rooms-test.sql](https://github.com/admsht/cs451-team-project/blob/main/tests/view-available-room-test.sql)
 
## Retrospective Summary
Here's what went well:
  * All work was completed smoothly and timely
  * There were no major issues during this sprint

Here's what we'd like to improve:
  * Group communication was challenging due to spring break and conflicting schedules

Here are changes we plan to implement in the next sprint:
  * Establish more consistent group meetings to improve communication
  * Continue implementing the frontend and integrate it with our database functionality
  * Maintain best practices with our SQL code to ensure smooth translation into our PostgreSQL database
