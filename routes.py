import datetime
from flask import Blueprint, current_app, request, jsonify, render_template
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import decode_token
from extensions import db  # Import db from the newly created extensions.py file
import jwt
from model import User  # Import the User model

# Helper function to decode the JWT token and validate the user
def validate_token(request):
    auth_header = request.headers.get('Authorization', None)  # Extract the authorization header
    if not auth_header:
        return None, jsonify({"error": "Token is missing!"}), 401  # Return error if token is missing

    try:
        token = auth_header.split(" ")[1]  # Split the header and get the token (format: "Bearer <token>")
        decoded_token = decode_token(token)  # Decode the JWT token

        # Find the user by email (or any unique identifier stored in the token)
        user = User.query.filter_by(email=decoded_token['sub']).first()
        if not user:
            return None, jsonify({"error": "User not found!"}), 404  # Return error if user not found
        return user, None  # Return the user if the token is valid

    except Exception as e:
        return None, jsonify({"error": f"Token error: {str(e)}"}), 401  # Return error if token validation fails


# Define a blueprint for routing (modularizes the app's routes)
routes_blueprint = Blueprint('routes', __name__)

# Default route to serve the index.html file (home page)
@routes_blueprint.route('/')
def index():
    return render_template('index.html')  # Render the index.html template when accessing '/'

# Route to create a new user
@routes_blueprint.route('/users', methods=['POST'])
def create_user():
    data = request.json  # Extract the incoming JSON data
    email = data.get('email')
    name = data.get('name')
    password = data.get('password')

    # Validate input data
    if not email or not name or not password:
        return jsonify({"error": "Missing email, name, or password"}), 400

    # Check if user with the provided email already exists
    existing_user = User.query.filter_by(email=email).first()
    if existing_user:
        return jsonify({"error": "User with that email already exists"}), 400

    # Hash the password
    hashed_password = generate_password_hash(password, method='sha256')

    # Create the new user
    new_user = User(email=email, name=name, password=hashed_password)
    db.session.add(new_user)
    db.session.commit()

    return jsonify({"message": "User created successfully!"}), 201

# Route to edit an existing user
@routes_blueprint.route('/users/<int:user_id>', methods=['PUT'])
def edit_user(user_id):
    user, error_response = validate_token(request)
    if error_response:
        return error_response

    data = request.json
    email = data.get('email')
    name = data.get('name')
    password = data.get('password')

    # Find the user by ID
    user_to_update = User.query.get(user_id)
    if not user_to_update:
        return jsonify({"error": "User not found"}), 404

    # Update user details
    if email:
        user_to_update.email = email
    if name:
        user_to_update.name = name
    if password:
        user_to_update.password = generate_password_hash(password, method='sha256')

    db.session.commit()
    return jsonify({"message": "User updated successfully!"}), 200

# Route to delete a user
@routes_blueprint.route('/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    user, error_response = validate_token(request)
    if error_response:
        return error_response

    # Find the user by ID
    user_to_delete = User.query.get(user_id)
    if not user_to_delete:
        return jsonify({"error": "User not found"}), 404

    db.session.delete(user_to_delete)
    db.session.commit()

    return jsonify({"message": "User deleted successfully!"}), 200

# Route to get all users
@routes_blueprint.route('/users', methods=['GET'])
def get_all_users():
    user, error_response = validate_token(request)  # Validate the user's token
    if error_response:
        return error_response  # Return error if the token validation fails

    # Fetch all users from the database
    users = User.query.all()

    # Create a list of dictionaries with user details
    result = [{"id": u.id, "email": u.email, "name": u.name} for u in users]

    return jsonify(result), 200  # Return the list of users
