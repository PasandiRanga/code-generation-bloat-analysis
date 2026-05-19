def calculate_pr_priority(days_waiting, comments, is_urgent):
    # Base score calculation
    score = (days_waiting * 5) + (comments * 2)
    
    # Double the score if urgent
    if is_urgent:
        score *= 2
    
    return score


# Example usage
days = int(input("Enter number of days waiting: "))
comments = int(input("Enter number of comments: "))
urgent = input("Is it urgent? (True/False): ").strip().lower() == "true"

priority_score = calculate_pr_priority(days, comments, urgent)
print("Priority Score:", priority_score)