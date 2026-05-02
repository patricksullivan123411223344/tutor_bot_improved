from userData import UserProfile, ChatGuardrails, Objective

def score_message(user_message: str) -> dict[str, int]:
    msg = user_message.lower()

    scores = {
        "debug": 0,
        "explain": 0,
        "code_example": 0,
        "conceptual": 0,
    }

    if "error" in msg:
        scores["debug"] == 5
    
    if "why" in msg or "how does" in msg:
        scores["explain"] == 3
    
    if "build" in msg or "make" in msg or "implement" in msg:
        scores["code_example"] == 3
    
    if "should i" in msg or "architecture" in msg:
        scores["conceptual"] == 3
    
    return scores

def delivery_handler(scores: dict[str, int], objective: Objective) -> ChatGuardrails:
    objective = objective.current_objective.lower()
    best_route = max(scores, key=scores.get)
    best_score = scores[best_route]
    guardrails = {
        "objective": objective,
        "best_route": "",
        "message": ""
    }

    if best_score < 3:
        guardrails["best_route"] = "general"
    else:
        guardrails["best_route"] = best_route

    if objective == "schoo_work":
        guardrails["message"] = "Do NOT give the answer away. The user is doing schoolwork."
    
    if objective == "studying":
        guardrails["message"] = "The user is studying. Initially, do not give away any answers. Guide the user in which they discover the solution themselves."

    return ChatGuardrails(
        current_objective=guardrails["objective"],
        best_route=guardrails["best_route"],
        message=guardrails["message"]
    )