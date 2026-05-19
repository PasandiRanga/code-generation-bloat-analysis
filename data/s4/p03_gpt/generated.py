def calculate_pr_priority(days_waiting, num_comments, is_urgent):
    # Calculate base score
    score = (days_waiting * 5) + (num_comments * 2)
    
    # Double score if urgent
    if is_urgent:
        score *= 2
    
    return score