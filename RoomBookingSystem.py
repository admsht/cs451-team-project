from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy
import os
from functools import wraps
from flask_migrate import Migrate

app = Flask(__name__)
app.secret_key = os.urandom(24)  # Generate a random secret key

# Configure PostgreSQL connection
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:123456@localhost:5432/room_booking'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize extensions
db = SQLAlchemy(app)
migrate = Migrate(app, db)
bcrypt = Bcrypt(app)

# Define Student model
class Student(db.Model):
    __tablename__ = 'Student'
    studentID = db.Column(db.Integer, primary_key=True)
    firstName = db.Column(db.String(50), nullable=False)
    lastName = db.Column(db.String(50), nullable=False)
    sEmail = db.Column(db.String(100), unique=True, nullable=False)
    sPassword = db.Column(db.String(100), nullable=False)
    
    # Relationships
    phone_numbers = db.relationship('StudentPhoneNumbers', backref='student', lazy=True, cascade="all, delete")
    bookings = db.relationship('Booking', backref='student', lazy=True, cascade="all, delete")
    repair_requests = db.relationship('RepairRequest', backref='student', lazy=True, cascade="all, delete")

    def __repr__(self):
        return f'<Student {self.firstName} {self.lastName}>'

# Define StudentPhoneNumbers model
class StudentPhoneNumbers(db.Model):
    __tablename__ = 'studentphonenumbers'
    studentID = db.Column(db.Integer, db.ForeignKey('Student.studentID'), primary_key=True)
    phoneNumber = db.Column(db.String(20), primary_key=True)

# Define Room model
class Room(db.Model):
    __tablename__ = 'room'
    roomNumber = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String(100))
    facility = db.Column(db.String(100))
    roomAvailability = db.Column(db.String(25), nullable=False)

    # Relationships
    bookings = db.relationship('Booking', backref='room', lazy=True, cascade="all, delete")
    repair_requests = db.relationship('RepairRequest', backref='room', lazy=True, cascade="all, delete")

# Define RepairRequest model
class RepairRequest(db.Model):
    __tablename__ = 'repairrequest'
    requestID = db.Column(db.Integer, primary_key=True)
    studentID = db.Column(db.Integer, db.ForeignKey('Student.studentID'), nullable=False)
    roomNumber = db.Column(db.Integer, db.ForeignKey('room.roomNumber'), nullable=False)
    description = db.Column(db.String(250))
    repairStatus = db.Column(db.String(25))

# Define Admin model
class Admin(db.Model):
    __tablename__ = 'admin'
    adminID = db.Column(db.Integer, primary_key=True)
    aEmail = db.Column(db.String(100), unique=True, nullable=False)
    aPassword = db.Column(db.String(100), nullable=False)

# Define Booking model
class Booking(db.Model):
    __tablename__ = 'booking'
    bookingID = db.Column(db.Integer, primary_key=True)
    studentID = db.Column(db.Integer, db.ForeignKey('Student.studentID'), nullable=False)
    roomNumber = db.Column(db.Integer, db.ForeignKey('room.roomNumber'), nullable=False)
    status = db.Column(db.String(25), nullable=False)
    bookingDate = db.Column(db.Date, nullable=False)

# Login required decorator
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('Please log in to access this page', 'danger')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

@app.route('/')
def index():
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        
        user = Student.query.filter_by(sEmail=email).first()
        
        if user:
            # Check if password is correct
            if bcrypt.check_password_hash(user.sPassword, password):
                session['user_id'] = user.studentID
                session['username'] = user.firstName
                flash('Login successful!', 'success')
                return redirect(url_for('dashboard'))
            else:
                flash('Invalid password', 'danger')
        else:
            flash('Email not found', 'danger')
    
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        first_name = request.form.get('first_name')
        last_name = request.form.get('last_name')
        email = request.form.get('email')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        
        # Simple validation
        existing_user = Student.query.filter_by(sEmail=email).first()
        if existing_user:
            flash('Email already exists', 'danger')
        elif password != confirm_password:
            flash('Passwords do not match', 'danger')
        else:
            # Hash the password and store user
            hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
            new_user = Student(
                firstName=first_name,
                lastName=last_name,
                sEmail=email,
                sPassword=hashed_password
            )
            
            # Add to database
            db.session.add(new_user)
            db.session.commit()
            
            flash('Registration successful! Please log in.', 'success')
            return redirect(url_for('login'))
    
    return render_template('register.html')

@app.route('/dashboard')
@login_required
def dashboard():
    user = Student.query.get(session['user_id'])
    booking = Booking.query.filter_by(studentID=user.studentID).first()
    
    return render_template('dashboard.html', username=session['username'], booking=booking)

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    flash('You have been logged out', 'info')
    return redirect(url_for('login'))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Create tables within app context
    app.run(debug=True)
