# routes/auth.py
from flask import Blueprint, request, jsonify, session
from werkzeug.security import generate_password_hash, check_password_hash

auth = Blueprint('auth', __name__)

# In-memory user store (replace with DB later)
users = {}

@auth.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    if username in users:
        return jsonify({"error": "Username already exists"}), 409

    hashed_password = generate_password_hash(password)
    users[username] = hashed_password
    return jsonify({"message": "User registered successfully"}), 201

@auth.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    hashed_password = users.get(username)
    if hashed_password and check_password_hash(hashed_password, password):
        session['user'] = username
        return jsonify({"message": "Login successful"}), 200
    else:
        return jsonify({"error": "Invalid credentials"}), 401

@auth.route('/logout', methods=['POST'])
def logout():
    session.pop('user', None)
    return jsonify({"message": "Logged out"}), 200

@auth.route('/user', methods=['GET'])
def get_current_user():
    user = session.get('user')
    if user:
        return jsonify({"user": user}), 200
    else:
        return jsonify({"error": "Not logged in"}), 401
