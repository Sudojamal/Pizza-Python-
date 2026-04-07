from flask import Flask, request, jsonify
import json
import os

app = Flask(__name__)

USERS_FILE = "users.json"

def load_users():
    """Load users from JSON file"""
    if os.path.exists(USERS_FILE):
        with open(USERS_FILE, "r") as f:
            return json.load(f)
    return {}

def save_users(users):
    """Save users to JSON file"""
    with open(USERS_FILE, "w") as f:
        json.dump(users, f, indent=4)

def init_users():
    """Initialize with default users if file doesn't exist"""
    if not os.path.exists(USERS_FILE):
        default_users = {
            "john": "password123",
            "jane": "securepass456",
            "admin": "admin123"
        }
        save_users(default_users)

@app.route("/login", methods=["POST"])
def login():
    """Handle login requests"""
    try:
        data = request.get_json()
        username = data.get("username", "").strip()
        password = data.get("password", "").strip()
        
        if not username or not password:
            return jsonify({"message": "Username and password are required"}), 400
        
        users = load_users()
        
        if username in users and users[username] == password:
            return jsonify({
                "message": "Login successful",
                "username": username,
                "status": "authenticated"
            }), 200
        else:
            return jsonify({"message": "Invalid username or password"}), 401
    
    except Exception as e:
        return jsonify({"message": f"Server error: {str(e)}"}), 500

@app.route("/register", methods=["POST"])
def register():
    """Handle user registration"""
    try:
        data = request.get_json()
        username = data.get("username", "").strip()
        password = data.get("password", "").strip()
        
        if not username or not password:
            return jsonify({"message": "Username and password are required"}), 400
        
        if len(password) < 6:
            return jsonify({"message": "Password must be at least 6 characters"}), 400
        
        users = load_users()
        
        if username in users:
            return jsonify({"message": "Username already exists"}), 409
        
        users[username] = password
        save_users(users)
        
        return jsonify({"message": "User registered successfully"}), 201
    
    except Exception as e:
        return jsonify({"message": f"Server error: {str(e)}"}), 500

@app.route("/health", methods=["GET"])
def health():
    """Health check endpoint"""
    return jsonify({"status": "Server is running"}), 200

if __name__ == "__main__":
    init_users()
    app.run(debug=True, host="localhost", port=5000)
