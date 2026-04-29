from flask import Flask, request, jsonify, render_template
from data import UserProfile
from tutorEngine import Tutor
import extractKeys
import loadSave
import os

user_handler = UserProfile(None, None, None, None)
tutor = Tutor("gemma3:1b")
app = Flask(__name__, static_folder="static")

@app.route("/")
def index():
    return render_template("chatbox.html")

if not os.path.exists("user_profiles/"):
    data = user_handler.first_contact()
    key = data.user_key
    loadSave.save_user_profile(data)
    user_profile = loadSave.load_user_profile(key)    
else:
    key = extractKeys.get_user_key()
    user_profile = loadSave.load_user_profile(key)

@app.route("/chat", methods=["POST"])
def chat():
    body = request.get_json()
    user_message = body.get("message", "").strip()

    if not user_message:
        return jsonify({"error": "Empty Message"}), 400
    
    response = tutor.respond(user_message, user_profile)

    return jsonify({"reply": response})

if __name__ == "__main__":
    app.run(debug=True)

