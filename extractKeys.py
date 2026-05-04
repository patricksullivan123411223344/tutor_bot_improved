import json
import os
import uuid

def create_user_key(user_name: str) -> str:
    """
    Create a unique user key from a username.
    Uses lowercase, stripped name as the identifier.
    In production, consider adding UUID suffix for collision handling.
    """
    slug = user_name.lower().strip().replace(" ", "_")
    return slug

def user_key_exists(user_key: str) -> bool:
    """Check if a user key already has a profile saved."""
    filepath = f"user_profiles/{user_key}_profile.json"
    return os.path.exists(filepath)

def save_user_key(user_key: str) -> str:
    """
    Save user key to file (deprecated - prefer session-based approach).
    Kept for backwards compatibility.
    """
    filepath = f"user_keys/{user_key}_key.json"
    data = {"user_key": user_key}

    if not os.path.exists(filepath):
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
    
    with open(filepath, "w") as f:
        json.dump(data, f, indent=4)
    
    return user_key

def get_user_key() -> str:
    """
    Get user key from file (deprecated - prefer session-based approach).
    This function is hardcoded to read patrick_key.json.
    In production, use Flask sessions instead.
    """
    filepath = "user_keys/patrick_key.json"

    with open(filepath, 'r') as f:
        key = json.load(f)
    
    return key["user_key"]