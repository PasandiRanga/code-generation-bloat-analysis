def calculate_pr_priority(days_waiting: int, num_comments: int, is_urgent: bool) -> int:
    """
    Calculate the priority score for a pull request.

    Args:
        days_waiting:  Number of days the PR has been waiting for review
        num_comments:  Number of comments on the PR
        is_urgent:     Whether the PR has been marked as urgent

    Returns:
        Final priority score as a whole number
    """
    score = (days_waiting * 5) + (num_comments * 2)

    if is_urgent:
        score *= 2

    return int(score)