from nlp.session import get_state
from nlp.health_score import calculate_health_score
from nlp.daily_progress import medication_adherence

def generate_triage_report(user_id: str) -> dict:
    # To get the state dictionary for the user
    data = get_state(user_id).get("data", {})

    # To return a structured dictionary instead of a formatted string
    return {
        "patient_id": user_id,
        "report_type": "Initial Triage",
        "symptoms": data.get('symptoms', 'N/A'),
        "duration": data.get('duration', 'N/A'),
        "severity": data.get('severity', 'N/A'),
        "age": data.get('age', 'N/A'),
        "pre_existing_conditions": data.get('conditions', 'N/A'),
        "allergies": data.get('allergies', 'N/A'),
        "current_medications": data.get('medications', 'N/A'),
        "recent_travel_exposure": data.get('exposure', 'N/A'),
        "approval_status": 0 # 0 = Pending for the professional dashboard
    }

def generate_followup_report(user_id: str, has_new_symptoms: bool) -> dict:
    # To calculate health score and adherence
    score = calculate_health_score(user_id)
    adherence = medication_adherence(user_id)

    # To build the base dictionary
    report_dict = {
        "patient_id": user_id,
        "report_type": "Comprehensive Follow-Up",
        "seven_day_health_score": score,
        "medical_adherence": adherence,
        "new_symptoms_reported": has_new_symptoms,
        "approval_status": 0 # 0 = Pending for the professional dashboard
    }

    # If there are new symptoms, to append the triage data
    if has_new_symptoms:
        checkup_data = generate_triage_report(user_id)
        # To add the triage data as a nested dictionary
        report_dict["checkup_details"] = checkup_data

    return report_dict