"""
Main entry point for the tutor bot application with interactive terminal interface.
This module orchestrates the tutoring session, manages user initialization, and handles the main chat loop.
"""

from userData import UserProfile, Objective
from tutorEngine import Tutor
import chatController
import extractKeys
import loadSaveProfile
import time
import sys
import os

def typing(msg: str, speed=0.05) -> str:
    # Simulate typing effect by printing characters with delay
    for char in msg:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(speed)
    print() # new line when finished

# List of stop words that terminate the tutoring session
stop_conditions = [
    "Bye",
    "Stop",
    "BYE",
    "STOP",
    "bye",
    "stop"
]

# Initialize handlers for user profile and learning objective
user_handler = UserProfile(None, None, None, None)
objective_handler = Objective(None)
# Create tutor instance with specified Ollama model
tutor = Tutor("gemma:7b")

typing("==== WELCOME TO THE TUTOR BOT ====")

# Check if first-time user or returning user
if not os.path.exists("user_profiles/"):
    # New user: gather initial profile information
    data = user_handler.first_contact()
    key = data.user_key
    loadSaveProfile.save_user_profile(data)
    user_profile = loadSaveProfile.load_user_profile(key)    
else:
    # Returning user: load existing profile
    typing("\n==== Loading user data ====")
    key = extractKeys.get_user_key()
    print(key)
    user_profile = loadSaveProfile.load_user_profile(key)
    print(user_profile)
    typing("\n==== Data loaded successfully ====")

# Prompt user to select their learning objective for this session
typing(f"Tutor: Hello {user_profile.user_name}, what is our objective today? (studying or school work)")
user_message = input("You: ")
typing("\n==== Setting objective =====")
# Set the objective for this tutoring session
objective_handler.set_objective(user_message)
typing("\n==== Objective set ====")
typing("\n==== Type bye or stop to exit ====")

if objective_handler.is_ready():
    try:
        # Main tutoring loop
        while True:
            user_message = input("You: ")
            # Check if user wants to end the session
            if user_message in stop_conditions:
                typing("Tutor: See you next time!")
                break
            # Get tutor response based on user message and context
            response = tutor.respond(user_message, user_profile, objective_handler)
            typing(f"Tutor: {response}")
            # Save the exchange to chat history for context in future responses
            chatController.save_chat_memory(user_message, response, user_profile.user_key)           
    except KeyboardInterrupt:
        # Handle premature session termination
        chatController.save_chat_memory(user_message, response, user_profile.user_key)
        typing("\nTutor: Session saved, now exiting.")

