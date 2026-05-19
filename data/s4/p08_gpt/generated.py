def calculate_pr_priority(days_waiting, comments_count, urgent):
    score = 0

    # Add 5 points for every waiting day
    score += days_waiting * 5

    # Add 2 points for every comment/commit left
    score += comments_count * 2

    # Double the score if marked urgent
    if urgent:
        score *= 2

    return int(score)