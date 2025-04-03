from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy
import os
from functools import wraps

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
    __tablename__ = 'users'  # Changed from default "user" to "users"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    student_id = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    
    def __repr__(self):
        return f'<User {self.username}>'

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

# Sample room data for admin dashboard demonstration.
rooms_data = [
    {
        'id': 101,
        'status': 'Occupied',
        'student': {'name': 'John Doe'},
        'check_in_date': '2025-04-01',
        'check_out_date': '2025-04-15',
        'room_type': 'Single'
    },
    {
        'id': 102,
        'status': 'Available',
        'student': None,
        'check_in_date': '',
        'check_out_date': '',
        'room_type': 'Double'
    },
    # Add more room records as needed.
]

# Landing page: let user choose login type.
@app.route('/')
def index():
    return render_template('index.html')

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
    return render_template('student_dashboard.html', username=session.get('username'))

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
    return render_template('admin_dashboard.html', rooms=rooms_data)

# Logout route for both admin and students.
@app.route('/logout')
def logout():
    session.pop('user_id', None)
    session.pop('username', None)
    session.pop('admin', None)
    flash('You have been logged out', 'info')
    return redirect(url_for('index'))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Create database tables if they don't exist.
    app.run(debug=True)
