from nlp.session import get_state, update_state, save_daily_report
from nlp.report import generate_followup_report
from nlp.initial_triage import triage_chat
import re

# Humanized daily check-in questions
FOLLOW_UP_QUESTIONS = [
    "Did you manage to take your medications as prescribed today? (Yes/No)",
    "Just thinking about your morning, afternoon, and evening routine—how many doses did you end up taking today?",
    "And how many doses were you supposed to take in total today?",
    "On a scale of 1 to 10, how are you feeling overall today? (1 being very poorly, and 10 being great!)",
    "Have you noticed any new symptoms popping up today? (Yes/No)"
]

def extract_number(text: str):
    """Safely extracts the first number found in a user's text input."""
    match = re.search(r'\d+', text)
    return int(match.group()) if match else None

def follow_up(user_id: str, user_input: str) -> str:
    session = get_state(user_id)
    step = session["step"]

    # --- Start Conversation ---
    if step == 0:
        update_state(user_id, 1)
        return FOLLOW_UP_QUESTIONS[0]

    # --- Question 1 ---
    elif step == 1:
        update_state(user_id, 2, "medication_taken", user_input.lower())
        return FOLLOW_UP_QUESTIONS[1]

    # --- Question 2 ---
    elif step == 2:
        num = extract_number(user_input)
        if num is None:
            return "Oops, I didn't quite catch a number there! Could you let me know how many doses you took today?"

        update_state(user_id, 3, "doses_taken", num)
        return FOLLOW_UP_QUESTIONS[2]

    # --- Question 3 ---
    elif step == 3:
        num = extract_number(user_input)
        if num is None:
            return "I just need a quick number for this one. How many doses were prescribed for today?"

        update_state(user_id, 4, "doses_expected", num)
        return FOLLOW_UP_QUESTIONS[3]

    # --- Question 4 ---
    elif step == 4:
        num = extract_number(user_input)
        if num is None or not (1 <= num <= 10):
            return "Could you give me a number between 1 and 10? How are you feeling overall today?"

        update_state(user_id, 5, "condition", num)
        return FOLLOW_UP_QUESTIONS[4]

    # --- Question 5 (FINAL) ---
    elif step == 5:
        has_new_symptoms = "yes" in user_input.lower()
        update_state(user_id, 0, "new_symptoms", "yes" if has_new_symptoms else "no")

        # Fetch fresh state after all updates
        session = get_state(user_id)
        data = session.get("data", {})

        # Save daily history
        daily_report = {
            "condition": data.get("condition", 0),
            "doses_taken": data.get("doses_taken", 0),
            "doses_expected": data.get("doses_expected", 0)
        }
        save_daily_report(user_id, daily_report)

        # Escalation decision
        if has_new_symptoms:
            # Passing a "start" trigger to triage so it initiates from question 1
            return triage_chat(user_id, "start")

        # Pass the boolean flag to match the refactored report.py logic
        return generate_followup_report(user_id, has_new_symptoms=False)

    return "Just checking in to see how you're doing today! 😊"