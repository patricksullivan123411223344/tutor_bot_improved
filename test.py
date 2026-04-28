from data import UserProfile
from tutorEngine import Tutor
import extractKeys
import loadSave
import os

user_handler = UserProfile(None, None, None, None)
tutor = Tutor("gemma3:1b")

stop_conditions = [
    "BYE",
    "STOP",
    "Bye",
    "Stop",
    "bye",
    "stop"
]

# TypeError: Object of type UserProfile is not JSON serializable
if not os.path.exists("user_profiles/"):
    data = user_handler.first_contact()
    key = data.user_key
    loadSave.save_user_profile(data)
    user_profile = loadSave.load_user_profile(key)    
else:
    key = extractKeys.get_user_key()
    user_profile = loadSave.load_user_profile(key)

while True:
  player_message = input("You: ")

  if player_message in stop_conditions:
     print("Goodbye...")
   
  response = tutor.respond(player_message, user_profile)
  print("Tutor Bot:", response.strip())




