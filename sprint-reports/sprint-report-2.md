# Sprint 2 Report 
Video Link:
## What's New (User Facing)
* **Admin Portal Implementation:**  
  Created a dedicated admin login and dashboard interface, allowing administrators to oversee room statuses, occupancy, and user assignments through a centralized view.
* **Enhanced Authentication System:**  
  Implemented role-based authentication that differentiates between student users and administrative staff, ensuring appropriate access control throughout the system.
* **Improved Database Integration:**  
  Refined the PostgreSQL database configuration and model definitions, ensuring proper table naming conventions and preventing conflicts with reserved keywords.

## Work Summary (Developer Facing)
During Sprint 2, our focus shifted to implementing the administrative components of our Room Booking System while refining our existing database and authentication infrastructure. We achieved this by:
* **Admin Authentication System:**  
  Developed specialized access controls that distinguish between student and administrative users, ensuring proper security protocols throughout the application.
* **Admin Dashboard Implementation:**  
  Created a functional admin dashboard that displays room occupancy data, enabling administrators to monitor and manage room assignments efficiently.
* **Database Structure Refinement:**  
  Improved our database model structure to avoid naming conflicts with PostgreSQL reserved keywords, resolving potential issues with table creation and queries.
* **Role-Based Access Control:**  
  Implemented custom decorators to restrict access to admin-only pages, ensuring that only authorized personnel can view or modify sensitive system information.
  

## Completed Issues/User Stories
Here are links to the issues that we completed in this sprint:

 * [Admin login page](https://github.com/users/admsht/projects/2/views/1?pane=issue&itemId=102929249&issue=admsht%7Ccs451-team-project%7C18)
 * [Admin dashboard](https://github.com/users/admsht/projects/2/views/1?pane=issue&itemId=102929697&issue=admsht%7Ccs451-team-project%7C20)

 
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
 * [app.py](https://github.com/admsht/cs451-team-project/blob/main/Project/app.py)
 * [admin_dashboard.html](https://github.com/admsht/cs451-team-project/blob/main/Project/templates/admin_dashboard.html)
 * [admin_login.html](https://github.com/admsht/cs451-team-project/blob/main/Project/templates/admin_login.html)
 
## Retrospective Summary
Here's what went well:
  * Successfully implemented the admin interface and role-based authentication
  * Improved database configuration to work better with PostgreSQL conventions
  * Better team coordination compared to Sprint 1 with more regular meetings

Here's what we'd like to improve:
  * Need better integration between frontend components and database models
  * Test coverage for admin functionality is currently insufficient

Here are changes we plan to implement in the next sprint:
  * Complete the remaining user stories focused on booking functionality and notifications
  * Implement proper model relationships between rooms, users, and bookings
  * Develop comprehensive testing for admin approval workflows
  * Finalize the student profile management system with proper validation
