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
        Format responses for a chat UI. We are using the marked node package.
        Use short paragraphs.
        Use numbered lists only when the user asks for steps.
        Prefer 1-3 bullets max.
        Do not bold entire questions.
        Do not over-explain.
        Sound like a helpful tutor, not a form.
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
