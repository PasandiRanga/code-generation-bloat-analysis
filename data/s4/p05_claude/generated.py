def calculate_priority_score(days_waiting: int, num_comments: int, is_urgent: bool) -> int:
    score = (days_waiting * 5) + (num_comments * 2)
    if is_urgent:
        score *= 2
    return score