def calculate_cafeteria_money(starting_amount: float, days: int) -> float:
    """
    Calculate remaining cafeteria money after a given number of days.
    
    - Days 1-7: Amount stays the same
    - Day 8 onwards: Amount loses 10% of its current value each day
    
    Args:
        starting_amount: Initial amount of money
        days: Number of days elapsed
    
    Returns:
        Final amount rounded to 2 decimal places
    """
    if days <= 7:
        return round(starting_amount, 2)
    
    decay_days = days - 7
    final_amount = starting_amount * (0.9 ** decay_days)
    
    return round(final_amount, 2)