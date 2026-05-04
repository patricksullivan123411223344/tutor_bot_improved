from userData import UserProfile, Objective
from tutorEngine import Tutor
import chatController
import extractKeys
import loadSaveProfile
import time
import sys
import os

def typing(msg: str, speed=0.05) -> str:
    for char in msg:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(speed)
    print() # new line when finished

stop_conditions = [
    "Bye",
    "Stop",
    "BYE",
    "STOP",
    "bye",
    "stop"
]

user_handler = UserProfile(None, None, None, None)
objective_handler = Objective(None)
tutor = Tutor("gemma:7b")

typing("==== WELCOME TO THE TUTOR BOT ====")

if not os.path.exists("user_profiles/"):
    data = user_handler.first_contact()
    key = data.user_key
    loadSaveProfile.save_user_profile(data)
    user_profile = loadSaveProfile.load_user_profile(key)    
else:
    typing("\n==== Loading user data ====")
    key = extractKeys.get_user_key()
    print(key)
    user_profile = loadSaveProfile.load_user_profile(key)
    print(user_profile)
    typing("\n==== Data loaded successfully ====")

typing(f"Tutor: Hello {user_profile.user_name}, what is our objective today? (studying or school work)")
user_message = input("You: ")
typing("\n==== Setting objective ====")
objective_handler.set_objective(user_message)
typing("\n==== Objective set ====")
typing("\n==== Type bye or stop to exit ====")

if objective_handler.is_ready():
    try:
        while True:
            user_message = input("You: ")
            if user_message in stop_conditions:
                typing("Tutor: See you next time!")
                break
            response = tutor.respond(user_message, user_profile, objective_handler)
            typing(f"Tutor: {response}")
            chatController.save_chat_memory(user_message, response, user_profile.user_key)           
    except KeyboardInterrupt:
        chatController.save_chat_memory(user_message, response, user_profile.user_key)
        typing("\nTutor: Session saved, now exiting.")

