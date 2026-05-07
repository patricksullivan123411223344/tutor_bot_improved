"""
Core tutoring engine that generates AI responses using Ollama and applies behavioral guardrails.
This module orchestrates message scoring, system prompt building, and response validation with feedback-based regeneration.
"""

import ollama 
import chatController 
import behaviorController
from userData import UserProfile, Objective, ChatGuardrails

class Tutor:
    def __init__(self, model):
        # Initialize with specified language model name
        self.model = model
        # Fallback message for when response generation fails
        self.fallback_reply = "I hit a response issue. Please try asking that one more time."

    @staticmethod
    def build_system_prompt(data: UserProfile, guardrails: ChatGuardrails) -> str:
        # Load recent chat history for context
        chat_handler = chatController.load_chat_memory(data.user_key)

        # Build comprehensive system prompt with user context, routing info, and chat history
        return f"""
        You are a helpful computer science tutor.

        USER STATE:
        Name: {data.user_name}
        Age: {data.user_age}
        Skill Level: {data.user_skill_level}
        Objective: {guardrails.current_objective}

        ROUTING STATE:
        Current route: {guardrails.best_route}
        Guardrail: {guardrails.message}

        CHAT CONTEXT:
        {chat_handler}
        
        IMPORTANT:
        If the user asks about their name, skill level, objective, or current session state,
        answer directly using USER STATE.
        You MUST refer to the user by their name.
        You MUST refer to the user's skill level.
        This is a PRIVATE SESSION and the user is aware that you have their information. 
        You are ALLOWED to refer to the user by their name, skill level, and objective.

        Now respond directly to the user's latest message.
        """
    
    def regenerate_with_feedback(self, user_message: str, data: UserProfile, original_reply: str, failures: list[str], guardrails: ChatGuardrails) -> str:
        # Build message chain including the original response and failure feedback
        messages = [
            {"role": "system", "content": self.build_system_prompt(data, guardrails)},
            {"role": "user", "content": user_message},
            {"role": "assistant", "content": original_reply},
            {
                "role": "user",
                # Ask model to revise response based on detected failures
                "content": (
                    "Please revise your last answer to fix the following issues\n" +
                    "\n".join(f"- {failure}" for failure in failures)
                )
            }
        ]

        # Request revised response from LLM
        reply = ollama.chat(
            model = self.model,
            messages=messages
        )

        # Extract and return regenerated response
        regenerated_reply = reply["message"]["content"].strip()
        return regenerated_reply if regenerated_reply else self.fallback_reply
        
    
    def respond(self, user_message: str, data: UserProfile, objective: Objective) -> str:
        # Score the user message to determine tutoring approach
        message_scores = behaviorController.score_message(user_message)

        # Determine guardrails based on message type and learning objective
        if message_scores:
            guardrails = behaviorController.delivery_handler(message_scores, objective)

        # Prepare message with system prompt and user input
        message = [{"role": "system", "content": self.build_system_prompt(data, guardrails)}]
        message.append({"role": "user", "content": user_message})

        # Get initial response from LLM
        response = ollama.chat(
            model = self.model,
            messages = message
        )

        # Extract and validate response
        original_reply = response["message"]["content"].strip()
        failures = chatController.validate_response(original_reply, data)

        # If validation fails, regenerate response with corrective feedback
        if failures:
            regenerated_reply = self.regenerate_with_feedback(
                user_message,
                data,
                original_reply,
                failures,
                guardrails
            )
            return regenerated_reply if regenerated_reply else self.fallback_reply
        
        # Return the validated original response
        return original_reply if original_reply else self.fallback_reply


