def calculate_priority_score(days_waiting, comments, urgent):
    score = (days_waiting * 5) + (comments * 2)
    
    if urgent:
        score *= 2
        
    return score