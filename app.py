from flask import Flask, jsonify, render_template, request, session
from userData import UserProfile, Objective
from tutorEngine import Tutor
import extractKeys
import loadSaveProfile
import chatController
import os

# Session configuration
app = Flask(__name__, static_folder="static")
app.secret_key = os.environ.get("SECRET_KEY", "dev-secret-key-change-in-production")
app.config["SESSION_COOKIE_HTTPONLY"] = True
app.config["SESSION_COOKIE_SECURE"] = False  # Set True in production with HTTPS
app.config["PERMANENT_SESSION_LIFETIME"] = 86400 * 7  # 7 days

tutor = Tutor("gemma:7b")

# Global objective handlers per user (in production, use database or Redis)
objective_handlers = {}

@app.route("/")
def index():
    return render_template("chatbox.html")

@app.route("/status", methods=["GET"])
def status():
    """Check if user is logged in, return user data or indicate onboarding needed."""
    if "user_key" not in session:
        return jsonify({"logged_in": False}), 200
    
    key = session["user_key"]
    try:
        user_profile = loadSaveProfile.load_user_profile(key)
        return jsonify({
            "logged_in": True,
            "user_name": user_profile.user_name,
            "user_age": user_profile.user_age,
            "user_skill_level": user_profile.user_skill_level
        }), 200
    except Exception as e:
        # User key in session but profile not found - clear session
        session.clear()
        return jsonify({"logged_in": False}), 200

@app.route("/onboard", methods=["POST"])
def onboard():
    """Create new user profile and start session."""
    data = request.get_json()
    name = data.get("name", "").strip()
    age = data.get("age", "").strip()
    skill_level = data.get("skill_level", "").strip()
    
    if not all([name, age, skill_level]):
        return jsonify({"error": "Missing required fields"}), 400
    
    # Generate unique key
    key = extractKeys.create_user_key(name)
    
    # Check if user already exists
    if loadSaveProfile.user_profile_exists(key):
        return jsonify({"error": "User already exists"}), 409
    
    try:
        # Create and save profile
        onboarding_info = UserProfile(
            user_key=key,
            user_name=name,
            user_age=age,
            user_skill_level=skill_level
        )
        loadSaveProfile.save_user_profile(onboarding_info)
        
        # Initialize objective handler for this user
        objective_handlers[key] = Objective(None)
        
        # Start session
        session.permanent = True
        session["user_key"] = key
        
        return jsonify({
            "success": True,
            "user_name": name
        }), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/set_objective", methods=["POST"])
def set_objective():
    """Set the user's learning objective."""
    if "user_key" not in session:
        return jsonify({"error": "Not logged in"}), 401
    
    key = session["user_key"]
    data = request.get_json()
    objective = data.get("objective")
    
    if key not in objective_handlers:
        objective_handlers[key] = Objective(None)
    
    try:
        objective_handlers[key].set_objective(objective)
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    
    return jsonify({
        "objective": objective_handlers[key].current_objective,
        "ready": objective_handlers[key].is_ready()
    }), 200

@app.route("/chat", methods=["POST"])
def chat():
    """Send message to tutor and get response."""
    if "user_key" not in session:
        return jsonify({"error": "Not logged in"}), 401
    
    key = session["user_key"]
    body = request.get_json()
    user_message = body.get("message", "").strip()
    
    if not user_message:
        return jsonify({"error": "Empty Message"}), 400
    
    try:
        # Load user profile
        user_profile = loadSaveProfile.load_user_profile(key)
        
        # Get objective handler
        if key not in objective_handlers:
            objective_handlers[key] = Objective(None)
        
        # Get response from tutor
        response = tutor.respond(user_message, user_profile, objective_handlers[key])
        
        if not isinstance(response, str) or not response.strip():
            return jsonify({"error": "Empty tutor reply"}), 502
        
        # Save chat memory
        chatController.save_chat_memory(user_message, response, key)
        
        return jsonify({"reply": response}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)