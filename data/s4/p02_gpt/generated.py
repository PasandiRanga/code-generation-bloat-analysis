def calculate_priority_score(days_waiting, comments, is_urgent):
    # Base score calculation
    score = (days_waiting * 5) + (comments * 2)

    # Double the score if marked as urgent
    if is_urgent:
        score *= 2

    return score


# Example usage
print(calculate_priority_score(4, 6, False))  # Output: 32
print(calculate_priority_score(4, 6, True))   # Output: 64