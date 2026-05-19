def calculate_pr_priority(days_waiting, comments, is_urgent):
    # Base score calculation
    score = (days_waiting * 5) + (comments * 2)

    # Double the score if urgent
    if is_urgent:
        score *= 2

    return score


# Example usage
print(calculate_pr_priority(4, 6, False))  # Output: 32
print(calculate_pr_priority(4, 6, True))   # Output: 64