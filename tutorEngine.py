import ollama 
import chatController 
from data import UserProfile, SessionState, TutorPayload

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
    
    def regenerate_with_feedback(self, user_message: str, data: UserProfile, original_reply: str, failures: list[str]) -> str:

        messages = [
            {"role": "system", "content": self.build_system_prompt(data)},
            {"role": "user", "content": user_message},
            {"role": "system", "content": original_reply},
            {
                "role": "user",
                "message": (
                    "Please revise your last answer to fix the following issues\n" +
                    "\n".join(f"- {failures}" for failure in failures)
                )
            }
        ]

        reply = ollama.chat(
            model = self.model,
            messages=messages
        )

        return reply["message"]["content"].strip()
        
    
    def respond(self, user_message: str, data: UserProfile) -> str:
        message = [{"role": "system", "content": self.build_system_prompt(data)}]
        message.append({"role": "user", "content": user_message})

        response = ollama.chat(
            model = self.model,
            messages = message
        )

        original_reply = response["message"]["content"].strip()
        failures = chatController.validate_response(original_reply, data)

        if failures:
            return self.regenerate_with_feedback(
                user_message,
                data,
                original_reply,
                failures
            )
        
        return original_reply


