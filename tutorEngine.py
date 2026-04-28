import ollama 
from data import UserProfile, SessionState

class Tutor:
    def __init__(self, model):
        self.model = model

    @staticmethod
    def build_system_prompt(data: UserProfile) -> str:
        return f"""
        You are a helpful computer science tutor.

        Here is your user information:
        Name: {data.user_name}
        Age: {data.user_age}
        Skill Level: {data.user_skill_level}

        Here is the current objective:

        
        Here is the players last move:


        And here is their friction level:


        Your task is to help the student with whatever they need in computer science based upon their requests and profile.
        You must refer to the student by their given name.
        """
    
    def respond(self, user_message: str, data: UserProfile) -> str:
        message = [{"role": "system", "content": self.build_system_prompt(data)}]
        message.append({"role": "user", "content": user_message})

        response = ollama.chat(
            model = self.model,
            messages = message
        )

        reply = response["message"]["content"].strip()
        return reply
