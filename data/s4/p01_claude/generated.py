def calculate_pr_priority(days_waiting: int, num_comments: int, is_urgent: bool) -> int:
    """
    Calculate the priority score for a pull request.

    Args:
        days_waiting (int): Number of days the PR has been waiting for review.
        num_comments (int): Number of comments left on the PR.
        is_urgent (bool): Whether the PR is marked as urgent.

    Returns:
        int: The priority score.
    """
    score = (days_waiting * 5) + (num_comments * 2)

    if is_urgent:
        score *= 2

    return score


if __name__ == "__main__":
    print("=== PR Priority Score Calculator ===\n")

    days = int(input("Days waiting: "))
    comments = int(input("Number of comments: "))
    urgent_input = input("Marked as urgent? (True/False): ").strip().lower()
    urgent = urgent_input in ("true", "yes", "1")

    score = calculate_pr_priority(days, comments, urgent)
    print(f"\nPriority Score: {score}")