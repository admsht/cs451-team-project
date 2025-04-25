# Sprint 3 Report 
Video Link:
## What's New (User Facing)
* **Updated Dashboard:**  
  The student dashboard now displays available rooms and the user is then able to request to book a room.
* **Updated Admin Dashboard:**  
  The admin dashboard now displays pending room requests, with the ability to approve or deny the request.

## Work Summary (Developer Facing)
During Sprint 3, our focus was primarily on implementing the remainder of our frontend features. We achieved this by:
* **Admin Dashboard Enhancement:**  
  Improved the admin dashboard, making it easier to manage room assignments.
* **Student Dashboard Enhancement:**
  The student dashboard has been updated to retrieve all available listings from the database and display them to the user.
* **Room Booking Implementation:**  
  Frontend client booking is now stored and retrieved from the backend database.
  

## Completed Issues/User Stories
Here are links to the issues that we completed in this sprint:

 * [Book Room](https://github.com/users/admsht/projects/2/views/1?pane=issue&itemId=100374707&issue=admsht%7Ccs451-team-project%7C5)
 * [Admin Booking Approval](https://github.com/users/admsht/projects/2/views/1?pane=issue&itemId=100374713&issue=admsht%7Ccs451-team-project%7C11)
 * [Admin Room Assignment](https://github.com/users/admsht/projects/2/views/1?pane=issue&itemId=100374712&issue=admsht%7Ccs451-team-project%7C10)

 
 ## Incomplete Issues/User Stories
Here are links to issues we worked on but did not complete in this sprint:

* [UserStory12: Admin Occupancy Reports](https://github.com/users/admsht/projects/2/views/1?pane=issue&itemId=100374714&issue=admsht%7Ccs451-team-project%7C12):  
  While we've begun displaying room data in the admin dashboard, comprehensive occupancy reports with filtering and export options are still in development.

* [UserStory9: Maintenance Update Notifications](https://github.com/users/admsht/projects/2/views/1?pane=issue&itemId=100374711&issue=admsht%7Ccs451-team-project%7C9):  
  The notification system for maintenance updates requires integration with the admin dashboard which is still being refined.

* [UserStory8: Booking Deadline Reminders](https://github.com/users/admsht/projects/2/views/1?pane=issue&itemId=100374710&issue=admsht%7Ccs451-team-project%7C8):  
  The reminder system requires implementation of a notification service that is still under development.


## Code Files for Review
Please review the following code files, which were actively developed during this sprint, for quality:
 * [app.py](https://github.com/admsht/cs451-team-project/blob/main/Project/app.py)
 * [admin_dashboard.html](https://github.com/admsht/cs451-team-project/blob/main/Project/templates/admin_dashboard.html)
 * [admin_login.html](https://github.com/admsht/cs451-team-project/blob/main/Project/templates/admin_login.html)
 * [student_dashboard.html](https://github.com/admsht/cs451-team-project/blob/main/Project/templates/student_dashboard.html)
 
## Retrospective Summary
Here's what went well:
  * Fully implemented room booking and approval system
  * Successfully configured our frontend to the database
  * Good team coordination

Here's what we'd like to improve:
  * Not all user stories were completed