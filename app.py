from flask import Flask, jsonify, render_template, request
from data import UserProfile
from tutorEngine import Tutor
import extractKeys
import loadSaveProfile
import os

user_handler = UserProfile(None, None, None, None)
tutor = Tutor("gemma3:1b")
app = Flask(__name__, static_folder="static")
appStart = True 

@app.route("/")
def index():
    return render_template("chatbox.html")
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

# need a way to get current objective 
# appStart will be true on first run
# we will get current objective if appStart == True
# ask objective
# appStart = False
# return objective as type str

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

