from data import SessionState, TutorPayload, UserProfile
import loadSaveProfile
import extractKeys
import json
import os

key = extractKeys.get_user_key()
user_controller = loadSaveProfile.load_user_profile(key)

## LOAD CHAT CONTEXT
def save_chat_memory(user_message: str, response: str, user_key: str) -> None:
    """Update the chat loop short term memory in here. Contains up to the last 10 chats."""
    filepath = f"/stm/{user_key}_chat_context"
    if os.path.exists(filepath):
        with open(filepath, "r") as f:
            data = json.load(f)
    else:
        data = []

    data.append({
        "user_message": user_message,
        "response": response
    })

    data = data[-10:]
    with open(filepath, "w") as f:
        json.dump(data)
    
def load_chat_memory(user_key: str) -> dict:
    filepath = f"stm/{user_key}_chat_context"

    try:
        with open(filepath, "r") as f:
            data = json.load(f)
            return data
    except FileNotFoundError:
        print(f"There is no value for the key: {user_key}")
        return None

## RESPONSE VALIDATION
def validate_response(reply: str, route: UserProfile) -> list[str]:
    print(route)
    failures = []
    skill = route.user_skill_level

    if skill in ["Beginner", "Intermediate"] and "```" not in reply:
        failures.append("Beginner or intermediate skill levels require shorter responses and room for self-discovery.")
    
    if "as an AI" in reply.lower():
        failures.append("Assistant-like speech detected. None of that phrasing is allowed.")
    
    return failures