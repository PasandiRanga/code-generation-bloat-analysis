def calculate_pr_priority(days: int, comments: int, urgent: bool) -> int:
    score = (days * 5) + (comments * 2)
    if urgent:
        score *= 2
    return score