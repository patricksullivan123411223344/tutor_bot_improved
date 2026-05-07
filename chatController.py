"""
Manages chat context storage, loading, and response validation for the tutor bot.
This module maintains a rolling window of recent chat exchanges and ensures responses meet quality guardrails.
"""

from userData import UserProfile
import loadSaveProfile
import extractKeys
import json
import os

key = extractKeys.get_user_key()
user_controller = loadSaveProfile.load_user_profile(key)

def save_chat_memory(user_message: str, response: str, user_key: str) -> None:
    """Update the chat loop short term memory in here. Contains up to the last 10 chats."""
    # Construct file path for this user's chat memory
    filepath = f"chat_memory/{user_key}_chat_context.json"
    # Load existing chat history or initialize empty list
    if os.path.exists(filepath):
        with open(filepath, "r") as f:
            data = json.load(f)
    else:
        data = []

    # Append new message-response pair
    data.append({
        "user_message": user_message,
        "response": response
    })

    # Keep only the last 10 exchanges for context
    data = data[-10:]
    with open(filepath, "w") as f:
        json.dump(data, f, indent=4)

def load_chat_memory(user_key: str) -> dict:
    # Construct file path for this user's chat memory
    filepath = f"chat_memory/{user_key}_chat_context.json"
    try:
        with open(filepath, "r") as f:
            data = json.load(f)
            return data
    except FileNotFoundError:
        print(f"There is no file for the key: {user_key}. Please save initial chat data.")
        return None

def validate_response(reply: str, route: UserProfile) -> list[str]:
    print(route)
    failures = []
    # Get user's skill level to determine response constraints
    skill = route.user_skill_level

    # Check for overly long responses for beginner/intermediate learners
    if skill in ["Beginner", "Intermediate"] and len(reply) > 900:
        failures.append("Beginner or intermediate skill levels require shorter responses and room for self-discovery.")
    
    # Prevent generic AI assistant language
    if "as an AI" in reply.lower():
        failures.append("Assistant-like speech detected. None of that phrasing is allowed.")
    
    return failures

