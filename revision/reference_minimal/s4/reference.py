def pr_priority(days, comments, urgent):
    return (days * 5 + comments * 2) * (2 if urgent else 1)
