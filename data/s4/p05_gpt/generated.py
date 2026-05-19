def calculate_priority_score(days_waiting, comments, urgent):
    # Base score calculation
    score = (days_waiting * 5) + (comments * 2)

    # Double the score if marked as urgent
    if urgent:
        score *= 2

    return int(score)


# Example usage
print(calculate_priority_score(4, 3, False))  # Output: 26
print(calculate_priority_score(4, 3, True))   # Output: 52