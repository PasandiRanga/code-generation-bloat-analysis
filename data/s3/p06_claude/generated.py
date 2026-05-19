def calculate_balance(starting_amount: float, days_passed: int) -> float:
    """
    Calculate remaining balance after decay.
    
    Decay starts on day 8: each day from day 8 onward,
    10% of the current balance decays (90% remains).
    
    Args:
        starting_amount: Initial amount of digital money
        days_passed: Number of days that have passed
    
    Returns:
        Remaining balance rounded to 2 decimal places
    """
    decay_days = max(0, days_passed - 7)  # Days 1-7 have no decay
    balance = starting_amount * (0.9 ** decay_days)
    return round(balance, 2)