def calculate_priority_score(waiting_days, comments, urgent):
    # Calculate base score
    score = (waiting_days * 5) + (comments * 2)

    # Double the score if urgent
    if urgent:
        score *= 2

    return score