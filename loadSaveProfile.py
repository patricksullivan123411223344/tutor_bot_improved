from userData import UserProfile
import json
import os 

def save_user_profile(data: UserProfile) -> None:
    key = data.user_key
    # data to save
    d2s = {
            "user_name": data.user_name,
            "user_age": int(data.user_age),
            "user_key": data.user_key,
            "user_skill_level": data.user_skill_level,
        }
    filepath = f"user_profiles/{key}_profile.json"

    if not os.path.exists(filepath):
        os.makedirs(os.path.dirname(filepath), exist_ok=True)    
    with open(filepath, 'w') as f:
        json.dump(d2s, f, indent=4)
          
def load_user_profile(key: str) -> UserProfile:
    filepath = f"user_profiles/{key}_profile.json"

    with open(filepath, "r") as f:
        data = json.load(f)
        
    return UserProfile(
        user_key = key,
        user_name = data["user_name"],
        user_age = data["user_age"],
        user_skill_level = data["user_skill_level"]
    )
    