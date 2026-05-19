def calculate_priority_score(days_waiting: int, comments: int, urgent: bool) -> int:
    score = (days_waiting * 5) + (comments * 2)
    if urgent:
        score *= 2
    return int(score)