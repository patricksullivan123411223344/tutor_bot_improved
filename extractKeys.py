import json
import os

# create a user key based on the given name input from the UserProfilePayload
def create_user_key(user_name: str) -> str:
    return user_name.lower().strip()

# take the user key from the create_user_key function and save it into the user_keys directory inside of their own respective
# file based upon their user key that was generated 
def save_user_key(user_key: str) -> None:
    filepath = f"user_keys/{user_key}_key.json"
    data = {"user_key": user_key}

    if not os.path.exists(filepath):
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
    
    with open(filepath, "w") as f:
        json.dump(data, f, indent=4)

def get_user_key() -> str:
    filepath = "user_keys/patrick_key.json"

    with open(filepath, 'r') as f:
        key = json.load(f)
    
    return key["user_key"]

