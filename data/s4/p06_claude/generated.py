def calculate_priority_score(days_waiting: int, num_comments: int, is_urgent: bool) -> int:
    """
    Calculate the priority score for a pull request.

    Args:
        days_waiting:  Number of days the PR has been waiting for review.
        num_comments:  Number of comments on the PR.
        is_urgent:     Whether the team has marked the PR as urgent.

    Returns:
        The calculated priority score.
    """
    score = (days_waiting * 5) + (num_comments * 2)

    if is_urgent:
        score *= 2

    return score