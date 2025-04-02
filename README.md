# cs451-team-project Room Booking System

This project is a Room Booking System built using Flask, SQLAlchemy, and PostgreSQL. It features separate login flows for students and admins. Students can register and log in, while admins use a hard-coded credential (for demonstration purposes) to access the admin dashboard.

## Prerequisites

- **Python 3.9+**
- **PostgreSQL**  
  You can install PostgreSQL via the [EDB Installer](https://www.enterprisedb.com/downloads/postgres-postgresql-downloads) or using Homebrew on macOS:
  ```bash
  brew install postgresql
  brew services start postgresql
  ```

## Getting Started

1. **Clone the Repository**
   ```bash
   git clone <repository-url>
   cd <repository-directory>
   ```

2. **Set Up the Virtual Environment**

   Create a virtual environment in the project root:
   ```bash
   python -m venv venv
   ```
   
   Activate the virtual environment:

   **macOS/Linux:**
   ```bash
   source venv/bin/activate
   ```

   **Windows:**
   ```bash
   venv\Scripts\activate
   ```

3. **Install Dependencies**
   
   Install the required packages using pip:
   ```bash
   pip install Flask Flask-Bcrypt Flask-SQLAlchemy psycopg2-binary
   ```
   If a `requirements.txt` file is provided, run:
   ```bash
   pip install -r requirements.txt
   ```

## Configuring PostgreSQL

1. **Create the Database**

   The application is configured to connect to a PostgreSQL database. By default, the connection string in `app.py` is:
   ```python
   app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://adams:post@localhost:5432/postgres'
   ```
   **Option A:** Use the default postgres database (ensure that your PostgreSQL user credentials match your environment).

   **Option B:** Create a new database (e.g., `room_booking`) using the command line:
   ```bash
   createdb room_booking -U <your_postgres_user>
   ```
   If you create a new database, update the connection string in `app.py` accordingly:
   ```python
   app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://<your_postgres_user>:<your_password>@localhost:5432/room_booking'
   ```

2. **Table Creation**

   When you run the Flask app, the code calls `db.create_all()` within the application context to create the required tables. The User model is explicitly mapped to the table `users` (to avoid conflicts with PostgreSQL’s reserved word user):
   ```python
   class User(db.Model):
       __tablename__ = 'users'
       id = db.Column(db.Integer, primary_key=True)
       username = db.Column(db.String(80), unique=True, nullable=False)
       password = db.Column(db.String(120), nullable=False)
       student_id = db.Column(db.String(20), nullable=False)
       email = db.Column(db.String(120), nullable=False)
       
       def __repr__(self):
           return f'<User {self.username}>'
   ```
   If you don’t see any tables in pgAdmin, you can force table creation by running a Flask shell:
   ```bash
   flask shell
   ```
   Then, in the shell:
   ```python
   from app import db
   db.create_all()
   ```

## Running the Application

1. **Ensure your virtual environment is activated.**

2. **Start the Flask Application:**
   ```bash
   flask run
   ```
   The application will run on [http://127.0.0.1:5000](http://127.0.0.1:5000).

3. **Access the Application:**

   **Landing Page:**  
   Choose between Student Login and Admin Login.

   **Student Flow:**
   - **Register:** Visit `/register` to create a new account.
   - **Login:** Visit `/login` to log in using your registered credentials.

   **Admin Flow:**
   - **Admin Login:** Visit `/admin/login` and log in using the sample admin credentials:
     - **Username:** admin
     - **Password:** adminpass

## Troubleshooting

- **No Tables Created:**  
  Make sure `db.create_all()` is executed by restarting the Flask app or running it manually in the Flask shell.

- **Database Connection Issues:**  
  Verify your connection string in `app.py` matches your PostgreSQL setup. Ensure the specified database exists.

- **Virtual Environment Issues:**  
  Ensure that the virtual environment is activated before running the Flask server.