def pr_priority(days: int, comments: int, urgent: bool) -> int:
    if days < 0 or comments < 0:
        return "Values cannot be negative"
    return ((days * 5) + (comments * 2)) * (2 if urgent else 1)

