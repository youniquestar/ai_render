from nlp.session import get_history

def calculate_health_score(user_id):

    history = get_history(user_id)

    if not history:
        return 0

    total = 0
    count = 0

    for day in history:
        score = int(day.get("condition", 0))
        total += score
        count += 1

    if count == 0:
        return 0

    avg = total / count

    # convert 1-10 scale → percentage
    percent = (avg / 10) * 100
    return round(percent, 2)