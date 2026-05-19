def calculate_pr_priority_score(waiting_days: int, num_comments: int, is_urgent: bool) -> int:
    score = (waiting_days * 5) + (num_comments * 2)
    if is_urgent:
        score *= 2
    return score