from nlp.session import get_history

def medication_adherence(user_id):

    history = get_history(user_id)

    taken = 0
    prescribed = 0

    for day in history:
        taken += day.get("doses_taken", 0)
        prescribed += day.get("doses_expected", 0)

    if prescribed == 0:
        return "No prescription data"

    return f"{taken} / {prescribed}"