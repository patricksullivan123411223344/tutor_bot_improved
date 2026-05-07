"""
Analyzes user messages to determine the best tutoring approach and applies appropriate guardrails.
This module scores incoming messages for keywords and routes them to the most suitable response strategy.
"""

from userData import UserProfile, ChatGuardrails, Objective

def score_message(user_message: str) -> dict[str, int]:
    # Convert message to lowercase for case-insensitive keyword matching
    msg = user_message.lower()

    # Initialize score counters for different tutoring approaches
    scores = {
        "debug": 0,
        "explain": 0,
        "code_example": 0,
        "conceptual": 0,
    }

    # Check for debugging-related keywords
    if "error" in msg:
        scores["debug"] == 5
    
    # Check for explanation-seeking keywords
    if "why" in msg or "how does" in msg:
        scores["explain"] == 3
    
    # Check for code implementation-related keywords
    if "build" in msg or "make" in msg or "implement" in msg:
        scores["code_example"] == 3
    
    # Check for conceptual/design pattern keywords
    if "should i" in msg or "architecture" in msg:
        scores["conceptual"] == 3
    
    return scores

def delivery_handler(scores: dict[str, int], objective: Objective) -> ChatGuardrails:
    # Extract and normalize the current learning objective
    objective = objective.current_objective.lower()
    # Identify the tutoring approach with the highest score
    best_route = max(scores, key=scores.get)
    best_score = scores[best_route]
    # Initialize guardrails dictionary with current objective
    guardrails = {
        "objective": objective,
        "best_route": "",
        "message": ""
    }

    # If no strong keyword match, default to general response
    if best_score < 3:
        guardrails["best_route"] = "general"
    else:
        guardrails["best_route"] = best_route

    # Set guardrail message based on learning objective
    if objective == "school_work":
        # For schoolwork, enforce non-answer-giving guidance
        guardrails["message"] = "Do NOT give the answer away. The user is doing schoolwork."
    
    if objective == "studying":
        # For studying, guide discovery-based learning
        guardrails["message"] = "The user is studying. Initially, do not give away any answers. Guide the user in which they discover the solution themselves."

    # Return guardrails object with determined route and message
    return ChatGuardrails(
        current_objective=guardrails["objective"],
        best_route=guardrails["best_route"],
        message=guardrails["message"]
    )