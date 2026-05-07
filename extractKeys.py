"""
Handles user key generation and retrieval for profile management.
This module creates normalized user keys from names and manages access to stored user authentication data.
"""

import json
import os

def create_user_key(user_name: str) -> str:
    # Normalize name by converting to lowercase and removing whitespace
    return user_name.lower().strip()

def save_user_key(user_key: str) -> None:
    # Construct file path for storing the user key
    filepath = f"user_keys/{user_key}_key.json"
    data = {"user_key": user_key}

    # Create directory structure if it doesn't exist
    if not os.path.exists(filepath):
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
    
    with open(filepath, "w") as f:
        json.dump(data, f, indent=4)

def get_user_key() -> str:
    # Load the currently active user's key from storage
    filepath = "user_keys/patrick_key.json"

    with open(filepath, 'r') as f:
        key = json.load(f)
    
    # Return the extracted user key string
    return key["user_key"]