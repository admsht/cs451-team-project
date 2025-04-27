from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy
import os
from functools import wraps
from datetime import date, datetime

app = Flask(__name__)
app.secret_key = os.urandom(24)  # Generate a random secret key

# Configure PostgreSQL connection
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://adams:post@localhost:5432/postgres'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize extensions
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)

# Define User model for students with an explicit table name to avoid reserved keywords
class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    student_id = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    
    def __repr__(self):
        return f'<User {self.username}>'

# Model for tracking maintenance and repair requests submitted by students
class RepairRequest(db.Model):
    __tablename__ = 'repair_requests'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)
    repair_type = db.Column(db.String(50), nullable=False)
    description = db.Column(db.Text, nullable=False)
    urgency = db.Column(db.String(20), nullable=False)
    status = db.Column(db.String(20), default='pending')
    date_submitted = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<RepairRequest {self.id}>'

# Model for the rooms in the system for students to book
class Room(db.Model):
    __tablename__ = 'Room'
    roomNumber = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String(100), nullable=False)
    facility = db.Column(db.String(100), nullable=False)
    roomAvailability = db.Column(db.String(25), nullable=False, server_default='Available', doc="CHECK (roomAvailability IN ('Available','Not Available'))")

    def __repr__(self):
        return f'<Room {self.roomNumber} ({self.roomAvailability})>'

# Model for the rooms in the system for admin to set status
class Booking(db.Model):
    __tablename__ = 'Booking'
    bookingID   = db.Column(db.Integer, primary_key=True)
    studentID   = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    roomNumber  = db.Column(db.Integer, db.ForeignKey('Room.roomNumber', ondelete='CASCADE'), nullable = False)
    status = db.Column(db.String(25), nullable=False, server_default='Pending',
    doc = "CHECK (status IN ('Pending','Confirmed','Cancelled'))")
    bookingDate = db.Column(db.Date, nullable=False, default = date.today)
    student = db.relationship('User', backref='bookings')
    room    = db.relationship('Room', backref='bookings')

    def __repr__(self):
        return f'<Booking {self.bookingID}: student {self.studentID} → room {self.roomNumber}>'

# Model for notification system for student to get notice
class Notification(db.Model):
    __tablename__ = 'notifications'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    message = db.Column(db.Text, nullable=False)
    notification_type = db.Column(db.String(50), nullable=False)
    is_read = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    reference_id = db.Column(db.Integer, nullable=True)
    
    # Add relationship to User model
    user = db.relationship('User', backref='notifications')
    
    def __repr__(self):
        return f'<Notification {self.id}: {self.notification_type}>'

# Student login required decorator
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('Please log in to access this page', 'danger')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

# Admin login required decorator
def admin_login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'admin' not in session:
            flash('Please log in as admin to access this page', 'danger')
            return redirect(url_for('admin_login'))
        return f(*args, **kwargs)
    return decorated_function

# Landing page: let user choose login type.
@app.route('/')
def index():
    return render_template('index.html')

# Logout route for both admin and students.
@app.route('/logout')
def logout():
    session.pop('user_id', None)
    session.pop('username', None)
    session.pop('admin', None)
    flash('You have been logged out', 'info')
    return redirect(url_for('index'))

# Student login route
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = User.query.filter_by(username=username).first()
        if user and bcrypt.check_password_hash(user.password, password):
            session['user_id'] = user.id
            session['username'] = user.username
            flash('Login successful!', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid credentials', 'danger')
    return render_template('login.html')

# Student registration route
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        student_id = request.form.get('student_id')
        email = request.form.get('email')
        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            flash('Username already exists', 'danger')
        elif password != confirm_password:
            flash('Passwords do not match', 'danger')
        else:
            hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
            new_user = User(
                username=username,
                password=hashed_password,
                student_id=student_id,
                email=email
            )
            db.session.add(new_user)
            db.session.commit()
            flash('Registration successful! Please log in.', 'success')
            return redirect(url_for('login'))
    return render_template('register.html')

# Student dashboard route
@app.route('/student/dashboard')
@login_required
def dashboard():
    user_id = session.get('user_id')
    # Get recent notifications for display in dashboard
    notifications = Notification.query.filter_by(user_id=user_id).order_by(Notification.created_at.desc()).limit(5).all()
    # Count unread notifications
    unread_notifications_count = Notification.query.filter_by(user_id=user_id, is_read=False).count()
    
    return render_template('student_dashboard.html', 
                          username=session.get('username'),
                          notifications=notifications,
                          unread_notifications_count=unread_notifications_count)

# Route to the repair requests from students
@app.route('/student/dashboard/repair-requests')
@login_required
def view_repair_requests():
    user_id = session.get('user_id')
    # Fetch all repair requests for the current user
    repair_requests = RepairRequest.query.filter_by(user_id=user_id).order_by(RepairRequest.date_submitted.desc()).all()
    return render_template('student_repair_requests.html', repair_requests=repair_requests)

# Route to handle the submission of new repair requests from students
@app.route('/student/dashboard/repair-requests/submit-repair', methods=['POST'])
@login_required
def submit_repair():
    user_id = session.get('user_id')
    
    # Extract form data submitted by the student
    repair_type = request.form.get('repair_type')
    description = request.form.get('repair_description')
    urgency = request.form.get('repair_urgency')
    
    # Create a new RepairRequest object with the submitted data
    new_repair = RepairRequest(
        user_id=user_id,
        repair_type=repair_type,
        description=description,
        urgency=urgency,
        status='pending'
    )
    
    db.session.add(new_repair)
    db.session.commit()
    
    flash('Repair request submitted successfully!', 'success')
    return redirect(url_for('view_repair_requests'))

# route for booking a room
@app.route('/student/dashboard/book-room', methods=['GET', 'POST'])
@login_required
def book_room():
    if request.method == 'GET':
        # Get all available rooms
        available_rooms = Room.query.filter_by(roomAvailability='Available').all()
        
        # Extract unique room types and facilities for filters
        room_types = set(room.type for room in available_rooms)
        facilities = set(room.facility for room in available_rooms)
        
        # Get today's date for the date picker in ISO format (YYYY-MM-DD)
        today = date.today().isoformat()
        
        return render_template(
            'student_book_room.html', 
            rooms=available_rooms, 
            room_types=room_types, 
            facilities=facilities,
            today=today
        )

    # Handle POST request (creating a booking)
    if request.method == 'POST':
        room_num = int(request.form['roomNumber'])
        booking_date = datetime.strptime(request.form['bookingDate'], '%Y-%m-%d').date()
        student_id = session['user_id']

        # Check if room is still available
        room = Room.query.get(room_num)
        if not room or room.roomAvailability != 'Available':
            flash('That room is no longer available.', 'danger')
            return redirect(url_for('student_book_room'))

        # Create new booking with status 'Pending'
        new_booking = Booking(
            studentID=student_id,
            roomNumber=room_num,
            status='Pending',  # Changed from default to explicitly set status
            bookingDate=booking_date
        )
        
        # Update room availability
        #room.roomAvailability = 'Not Available'

        # Save to database
        db.session.add(new_booking)
        db.session.commit()

        flash(f'Room {room_num} booked successfully for {booking_date}', 'success')
        return redirect(url_for('dashboard'))

# Helper function to create notifications
def create_notification(user_id, message, notification_type, reference_id=None):
    notification = Notification(
        user_id=user_id,
        message=message,
        notification_type=notification_type,
        reference_id=reference_id
    )
    db.session.add(notification)
    db.session.commit()
    return notification

# Route for students to view their notifications
@app.route('/student/dashboard/notifications')
@login_required
def view_notifications():
    user_id = session.get('user_id')
    notifications = Notification.query.filter_by(user_id=user_id).order_by(Notification.created_at.desc()).all()
    return render_template('student_notifications.html', notifications=notifications)

# Route to mark a single notification as read
@app.route('/student/dashboard/notifications/mark-notification-read', methods=['POST'])
@login_required
def mark_notification_read():
    notification_id = request.form.get('notification_id')
    notification = Notification.query.get(notification_id)
    
    if notification and notification.user_id == session.get('user_id'):
        notification.is_read = True
        db.session.commit()
        flash('Notification marked as read', 'success')
    
    return redirect(url_for('view_notifications'))

# Route to mark all notifications as read
@app.route('/student/dashboard/notifications/mark-all-read', methods=['POST'])
@login_required
def mark_all_read():
    user_id = session.get('user_id')
    unread_notifications = Notification.query.filter_by(user_id=user_id, is_read=False).all()
    
    for notification in unread_notifications:
        notification.is_read = True
    
    db.session.commit()
    flash('All notifications marked as read', 'success')
    return redirect(url_for('view_notifications'))

# Route for students to view their bookings
@app.route('/student/dashboard/my-bookings')
@login_required
def view_bookings():
    user_id = session.get('user_id')
    bookings = Booking.query.filter_by(studentID=user_id).order_by(Booking.bookingDate.desc()).all()
    return render_template('student_view_bookings.html', bookings=bookings)

# Route to view booking details
@app.route('/booking/<int:booking_id>')
@login_required
def view_booking_details(booking_id):
    booking = Booking.query.get_or_404(booking_id)
    
    # Make sure the booking belongs to the logged-in user
    if booking.studentID != session.get('user_id'):
        flash('You do not have permission to view this booking', 'danger')
        return redirect(url_for('view_bookings'))
    
    return render_template('booking_details.html', booking=booking)

# Route for students to cancel their pending bookings
@app.route('/student/dashboard/my-bookings/cancel-booking', methods=['POST'])
@login_required
def cancel_booking():
    booking_id = request.form.get('booking_id')
    booking = Booking.query.get(booking_id)
    
    if not booking:
        flash('Booking not found', 'danger')
        return redirect(url_for('view_bookings'))
    
    # Verify ownership
    if booking.studentID != session.get('user_id'):
        flash('You do not have permission to cancel this booking', 'danger')
        return redirect(url_for('view_bookings'))
    
    # Only allow cancellation of pending bookings
    if booking.status != 'Pending':
        flash('You can only cancel pending bookings', 'danger')
        return redirect(url_for('view_bookings'))
    
    # Update booking status
    booking.status = 'Cancelled'
    
    # Make room available again
    room = Room.query.get(booking.roomNumber)
    room.roomAvailability = 'Available'
    
    db.session.commit()
    
    flash('Booking cancelled successfully', 'success')
    return redirect(url_for('view_bookings'))

# Admin login route
@app.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        admin_username = request.form.get('admin_username')
        admin_password = request.form.get('admin_password')
        # For demonstration, we hard-code admin credentials.
        if admin_username == 'admin' and admin_password == 'adminpass':
            session['admin'] = True
            flash('Admin login successful!', 'success')
            return redirect(url_for('admin_dashboard'))
        else:
            flash('Invalid admin credentials', 'danger')
    return render_template('admin_login.html')

# Admin dashboard route
@app.route('/admin/dashboard')
@admin_login_required
def admin_dashboard():
    return render_template('admin_dashboard.html', username=session.get('username'))

# Room Management route
@app.route('/admin/dashboard/room-management')
@admin_login_required
def room_management():
    # Get available rooms (not assigned to any student)
    available_rooms = Room.query.filter_by(roomAvailability='Available').all()
    
    # Get all registered students
    students = User.query.all()
    
    # Get pending bookings
    pending_bookings = Booking.query.filter_by(status='Pending').all()
    
     # Get confirmed bookings where the room is still available (not assigned yet)
    approved_bookings = db.session.query(Booking).join(Room, Booking.roomNumber == Room.roomNumber).filter(
        Booking.status == 'Confirmed',
        Room.roomAvailability == 'Available'
    ).all()

    # For occupancy reports
    total_rooms = Room.query.count()
    occupied_rooms = Room.query.filter_by(roomAvailability='Not Available').count()
    available_rooms_count = total_rooms - occupied_rooms
    occupancy_rate = round((occupied_rooms / total_rooms) * 100) if total_rooms > 0 else 0
    
    # Get room type distribution
    room_types = db.session.query(Room.type, db.func.count(Room.roomNumber)).group_by(Room.type).all()
    room_types_labels = [rt[0] for rt in room_types]
    
    # Count occupied rooms by type
    room_types_occupied = []
    room_types_available = []
    
    for rt in room_types_labels:
        occupied = Room.query.filter_by(type=rt, roomAvailability='Not Available').count()
        available = Room.query.filter_by(type=rt, roomAvailability='Available').count()
        room_types_occupied.append(occupied)
        room_types_available.append(available)
    
    # Get facilities distribution
    facilities = db.session.query(Room.facility, db.func.count(Room.roomNumber)).group_by(Room.facility).all()
    facilities_labels = [f[0] for f in facilities]
    facilities_occupancy = [f[1] for f in facilities]
    
    return render_template(
        'admin_room_management.html',
        available_rooms=available_rooms,
        students=students,
        pending_bookings=pending_bookings,
        approved_bookings=approved_bookings,
        total_rooms=total_rooms,
        occupied_rooms=occupied_rooms,
        available_rooms_count=available_rooms_count,
        occupancy_rate=occupancy_rate,
        room_types_labels=room_types_labels,
        room_types_occupied=room_types_occupied,
        room_types_available=room_types_available,
        facilities_labels=facilities_labels,
        facilities_occupancy=facilities_occupancy
    )

# Assign Room route - handles the room assignment form submission
@app.route('/admin/dashboard/room-management/assign-room', methods=['POST'])
@admin_login_required
def assign_room():
    room_id = request.form.get('room_id')
    student_id = request.form.get('student_id')
    check_in_date = request.form.get('check_in_date')
    check_out_date = request.form.get('check_out_date')
    
    # Verify that room and student exist
    room = Room.query.get(room_id)
    student = User.query.get(student_id)
    
    if not room or not student:
        flash('Invalid room or student selection', 'danger')
        return redirect(url_for('room_management'))
    
    # Check if room is available
    if room.roomAvailability != 'Available':
        flash('This room is no longer available', 'danger')
        return redirect(url_for('room_management'))
    
    # Create a new booking with 'Confirmed' status (direct assignment)
    new_booking = Booking(
        studentID=student_id,
        roomNumber=room_id,
        status='Confirmed',
        bookingDate=datetime.strptime(check_in_date, '%Y-%m-%d').date()
    )
    
    # Update room status
    room.roomAvailability = 'Not Available'
    
    # Save to database
    db.session.add(new_booking)
    db.session.commit()
    
    # Create notification for the student
    room_details = f"Room {room_id} ({room.type}, {room.facility})"
    notification_message = f"You have been assigned {room_details} starting on {check_in_date}."
    create_notification(
        user_id=student_id,
        message=notification_message,
        notification_type='room_assignment',
        reference_id=new_booking.bookingID
    )

    flash(f'Room {room_id} successfully assigned to {student.username}', 'success')
    return redirect(url_for('room_management'))

# Approve booking route
@app.route('/admin/dashboard/room-management/approve-booking', methods=['POST'])
@admin_login_required
def approve_booking():
    booking_id = request.form.get('booking_id')
    booking = Booking.query.get(booking_id)
    
    if not booking:
        flash('Booking not found', 'danger')
        return redirect(url_for('room_management'))
    
    # Update booking status
    booking.status = 'Confirmed'
    
    # Update room status
    
    #room.roomAvailability = 'Not Available'
    
    db.session.commit()

     # Create notification for the student
    room = Room.query.get(booking.roomNumber)
    room_details = f"Room {booking.roomNumber} ({room.type}, {room.facility})"
    notification_message = f"Your booking for {room_details} on {booking.bookingDate.strftime('%Y-%m-%d')} has been approved."
    create_notification(
        user_id=booking.studentID,
        message=notification_message,
        notification_type='booking_approval',
        reference_id=booking.bookingID
    )
    
    flash(f'Booking {booking_id} has been approved', 'success')
    return redirect(url_for('room_management'))

# Reject booking route
@app.route('/admin/dashboard/room-management/reject-booking', methods=['POST'])
@admin_login_required
def reject_booking():
    booking_id = request.form.get('booking_id')
    booking = Booking.query.get(booking_id)
    
    if not booking:
        flash('Booking not found', 'danger')
        return redirect(url_for('room_management'))
    
    # Update booking status
    booking.status = 'Cancelled'
    
    # Keep room available
    room = Room.query.get(booking.roomNumber)
    room.roomAvailability = 'Available'
    
    db.session.commit()
    
    # Create notification for the student
    room_details = f"Room {booking.roomNumber} ({room.type}, {room.facility})"
    notification_message = f"Your booking for {room_details} on {booking.bookingDate.strftime('%Y-%m-%d')} has been rejected."
    create_notification(
        user_id=booking.studentID,
        message=notification_message,
        notification_type='booking_rejection',
        reference_id=booking.bookingID
    )

    flash(f'Booking {booking_id} has been rejected', 'danger')
    return redirect(url_for('room_management'))

# route to finalize the room assignment for approved bookings
@app.route('/admin/dashboard/room-management/finalize-assignment', methods=['POST'])
@admin_login_required
def finalize_assignment():
    booking_id = request.form.get('booking_id')
    booking = Booking.query.get(booking_id)
    
    if not booking:
        flash('Booking not found', 'danger')
        return redirect(url_for('room_management'))
    
    # Check if booking status is confirmed
    if booking.status != 'Confirmed':
        flash('Only confirmed bookings can be assigned', 'danger')
        return redirect(url_for('room_management'))
    
    # Update room availability
    room = Room.query.get(booking.roomNumber)
    if room:
        room.roomAvailability = 'Not Available'
        
        # Create notification for the student
        room_details = f"Room {booking.roomNumber} ({room.type}, {room.facility})"
        notification_message = f"Your room has been assigned! {room_details} is now ready for your use on {booking.bookingDate.strftime('%Y-%m-%d')}."
        create_notification(
            user_id=booking.studentID,
            message=notification_message,
            notification_type='room_assignment',
            reference_id=booking.bookingID
        )
        
        db.session.commit()
        flash(f'Room {booking.roomNumber} has been successfully assigned to the student', 'success')
    else:
        flash('Room not found', 'danger')
    
    return redirect(url_for('room_management'))

# Admin Repair Requests Management route
@app.route('/admin/dashboard/repair-requests')
@admin_login_required
def admin_repair_requests():
    # Join the repair_requests and users tables to get student names
    repair_requests = db.session.query(
        RepairRequest,
        User.username.label('student_name')
    ).join(
        User, 
        RepairRequest.user_id == User.id
    ).order_by(
        RepairRequest.date_submitted.desc()
    ).all()
    
    # Convert the results to a list of dictionaries for easier template access
    repair_requests_data = []
    for request, student_name in repair_requests:
        request_dict = {
            'id': request.id,
            'user_id': request.user_id,
            'student_name': student_name,
            'repair_type': request.repair_type,
            'description': request.description,
            'urgency': request.urgency,
            'status': request.status,
            'date_submitted': request.date_submitted
        }
        repair_requests_data.append(request_dict)
    
    return render_template('admin_repair_requests.html', repair_requests=repair_requests_data)

# Update Repair Status route
@app.route('/admin/dashboard/repair-requests/update-repair-status', methods=['POST'])
@admin_login_required
def update_repair_status():
    request_id = request.form.get('request_id')
    new_status = request.form.get('new_status')
    status_notes = request.form.get('status_notes', '')
    
    # Validate input
    if not request_id or not new_status:
        flash('Invalid input', 'danger')
        return redirect(url_for('admin_repair_requests'))
    
    # Make sure status is valid
    valid_statuses = ['pending', 'in_progress', 'completed']
    if new_status not in valid_statuses:
        flash('Invalid status', 'danger')
        return redirect(url_for('admin_repair_requests'))
    
    # Find the repair request
    repair_request = RepairRequest.query.get(request_id)
    if not repair_request:
        flash('Repair request not found', 'danger')
        return redirect(url_for('admin_repair_requests'))
    
    # Get old status for notification message
    old_status = repair_request.status

    # Update the status
    repair_request.status = new_status
    
    # Create notification for the student
    repair_type_display = repair_request.repair_type.replace('_', ' ').capitalize()
    notification_message = f"Your repair request for {repair_type_display} has been updated from '{old_status.replace('_', ' ').capitalize()}' to '{new_status.replace('_', ' ').capitalize()}'."
    
    if status_notes:
        notification_message += f" Admin notes: {status_notes}"
    
    create_notification(
        user_id=repair_request.user_id,
        message=notification_message,
        notification_type='repair_update',
        reference_id=repair_request.id
    )
    
    db.session.commit()
    
    flash(f'Repair request status updated to {new_status.replace("_", " ").capitalize()}', 'success')
    return redirect(url_for('admin_repair_requests'))

if __name__ == '__main__':

    with app.app_context():
        db.create_all()  # Create database tables if they don't exist.

        # Add sample data if the Room table is empty
        if Room.query.count() == 0:

            # Create a list of sample rooms with different types and facilities
            rooms = [
                Room(roomNumber=101, type='Single', facility='Facility A'),
                Room(roomNumber=102, type='Single', facility='Facility A'),
                Room(roomNumber=103, type='Double', facility='Facility A'),
                Room(roomNumber=104, type='Double', facility='Facility A'),
                Room(roomNumber=201, type='Single', facility='Facility B'),
                Room(roomNumber=202, type='Single', facility='Facility B'),
                Room(roomNumber=203, type='Suite', facility='Facility B'),
                Room(roomNumber=204, type='Suite', facility='Facility B'),
                Room(roomNumber=301, type='Single', facility='Facility C'),
                Room(roomNumber=302, type='Double', facility='Facility C'),
                Room(roomNumber=303, type='Suite', facility='Facility C'),
                Room(roomNumber=304, type='Apartment', facility='Facility C'),
            ]
            
            # Add all sample rooms to the database
            db.session.bulk_save_objects(rooms)
            db.session.commit()

    app.run(debug=True)
