from nlp.session import get_state, update_state
from nlp.report import generate_triage_report

# Humanized questions for a friendly, caring onboarding experience
QUESTIONS = [
    "First, could you tell me a little bit about what you're feeling? What symptoms are you experiencing?",
    "I'm sorry you're having to deal with that. Roughly how long have you been feeling this way?",
    "On a scale of 1 to 10 (where 1 is very mild and 10 is unbearable), how severe would you say your symptoms are right now?",
    "Got it. To help me understand your situation better, what is your age?",
    "Do you have any pre-existing medical conditions that I should know about?",
    "Do you have any known allergies, especially to medications?",
    "Have you taken any medications recently to help with how you're feeling?",
    "And finally, have you traveled recently or been around anyone else who has been sick?"
]

def triage_chat(user_id: str, user_input: str) -> str:
    session = get_state(user_id)
    step = session["step"]

    # Start conversation
    if user_input.lower() in ["hi", "hello", "hey", "start"]:
        update_state(user_id, 1)
        return QUESTIONS[0]

    # Continue conversation and collect answers
    if 1 <= step <= len(QUESTIONS):
        keys = ["symptoms", "duration", "severity", "age", "conditions", "allergies", "medications", "exposure"]
        update_state(user_id, step + 1, keys[step - 1], user_input)

        if step < len(QUESTIONS):
            return QUESTIONS[step]
        else:
            # Generate the report after all questions are answered
            report = generate_triage_report(user_id)
            update_state(user_id, 0) # Reset the session
            return report

    return "Hello! My name is WellSync, your AI health partner. I'm here to help you figure out what's going on and get you on the right track."