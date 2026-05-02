from flask import Flask, jsonify, render_template, request
from userData import UserProfile, Objective
from tutorEngine import Tutor
import extractKeys
import loadSaveProfile
import os

user_handler = UserProfile(None, None, None, None)
objective_handler = Objective(None)
tutor = Tutor("gemma:7b")
app = Flask(__name__, static_folder="static")
appStart = True 

@app.route("/")
def index():
    return render_template("chatbox.html")

# We need to fix this as it is still the terminal based onboarding flow 
if not os.path.exists("user_profiles/"):
    data = user_handler.first_contact()
    key = data.user_key
    loadSaveProfile.save_user_profile(data)
    user_profile = loadSaveProfile.load_user_profile(key)    
else:
    key = extractKeys.get_user_key()
    print(key)
    user_profile = loadSaveProfile.load_user_profile(key)
    print(user_profile)

@app.route("/set_objective", methods=["POST"])
def set_objective():
    data = request.get_json()
    objective = data.get("objective")

    try:
        objective_handler.set_objective(objective)
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    
    return jsonify({
        "objective": objective_handler.current_objective,
        "ready": objective_handler.is_ready()
    })

@app.route("/chat", methods=["POST"])
def chat():
    body = request.get_json()
    user_message = body.get("message", "").strip()

    if not user_message:
        return jsonify({"error": "Empty Message"}), 400
    
    response = tutor.respond(user_message, user_profile, objective_handler)

    if not isinstance(response, str) or not response.strip():
        return jsonify({"error": "Empty tutor reply"}), 502

    return jsonify({"reply": response})

if __name__ == "__main__":
    app.run(debug=True)