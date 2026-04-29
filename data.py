from dataclasses import dataclass
from extractKeys import create_user_key

@dataclass 
class UserProfile:
    user_key: str
    user_name: str
    user_age: int
    user_skill_level: str

    def first_contact(self):
        print("==== Let's get some info before we start ====\n")
        name = input("What's your name?: ")
        key = create_user_key(name)
        age = input("What's your age?: ")
        skill_level = input("What's your skill level?: ")

        return UserProfile(
            user_key=key,
            user_name=name,
            user_age=age,
            user_skill_level=skill_level
        )

@dataclass
class SessionState:
    user_current_objective: str
    user_friction_score: str
    chat_context: dict

@dataclass
class TutorPayload:
    debugging: bool
    state: str

