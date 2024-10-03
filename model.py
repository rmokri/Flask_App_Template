from extensions import db  # Import db from extensions.py

# User model representing the 'user' table in the database
class User(db.Model):
    __tablename__ = 'user'  # Specifies the table name

    # Define the columns for the 'user' table
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)  # Primary key
    email = db.Column(db.String(120), unique=True, nullable=False)  # Email field, unique and required
    name = db.Column(db.String(120), nullable=False)  # Name field, required
    password = db.Column(db.String(128), nullable=False)  # Password field, required (hashed)
    description = db.Column(db.Text)  # Optional
