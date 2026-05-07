"""
Manages persistence of user profile data to and from JSON files.
This module handles serializing user information and loading profiles into memory for use during tutoring sessions.
"""

from userData import UserProfile
import json
import os 

def save_user_profile(data: UserProfile) -> None:
    # Extract the user key for file naming
    key = data.user_key
    # Prepare profile data dictionary for JSON serialization
    d2s = {
            "user_name": data.user_name,
            "user_age": int(data.user_age),
            "user_key": data.user_key,
            "user_skill_level": data.user_skill_level,
        }
    # Construct the file path for this user's profile
    filepath = f"user_profiles/{key}_profile.json"

    # Create directory structure if needed
    if not os.path.exists(filepath):
        os.makedirs(os.path.dirname(filepath), exist_ok=True)    
    # Write the profile data to JSON file
    with open(filepath, 'w') as f:
        json.dump(d2s, f, indent=4)
          
def load_user_profile(key: str) -> UserProfile:
    # Construct file path using the user key
    filepath = f"user_profiles/{key}_profile.json"

    # Load profile data from JSON file
    with open(filepath, "r") as f:
        data = json.load(f)
        
    # Reconstruct and return a UserProfile object from the loaded data
    return UserProfile(
        user_key = key,
        user_name = data["user_name"],
        user_age = data["user_age"],
        user_skill_level = data["user_skill_level"]
    )
    