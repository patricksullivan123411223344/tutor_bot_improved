"""
Defines core data structures for user profiles, learning objectives, and chat guardrails.
This module contains dataclasses that represent the state and preferences of users during tutoring sessions.
"""

from dataclasses import dataclass
from extractKeys import create_user_key
import time
import sys

def typing(msg: str, speed=0.05) -> str:
    # Simulate typing effect by printing characters with delay
    for char in msg:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(speed)
    print() # new line when finished

@dataclass 
class UserProfile:
    user_key: str
    user_name: str
    user_age: int
    user_skill_level: str

    def first_contact(self):
        # Gather initial user information during first session
        typing("==== Let's get some info before we start ====\n")

        name = input("What's your name?: ")
        key = create_user_key(name)
        age = input("What's your age?: ")
        skill_level = input("What's your skill level?: ")

        typing("==== Thank you! ====")

        return UserProfile(
            user_key=key,
            user_name=name,
            user_age=age,
            user_skill_level=skill_level
        )

@dataclass
class ChatGuardrails:
    # Container for guardrail instructions applied to tutor responses
    current_objective: str
    best_route: str
    message: str

@dataclass
class Objective:
    # Container for the user's learning objective during a session
    current_objective: str | None = None

    def set_objective(self, objective: str) -> None:
        # Validate and set the user's learning objective
        if objective not in ["studying", "school_work", "school work"]:
            raise ValueError("Invalid mode selected")
        self.current_objective = objective
        print(self.current_objective)

    def is_ready(self) -> bool:
        # Check if a valid objective has been set
        return self.current_objective is not None



