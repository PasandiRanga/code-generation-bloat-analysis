def remaining_balance(amount, days_passed):
    """
    Calculate remaining cafeteria balance after daily decay.
    
    Parameters:
    amount (float): Initial unspent amount
    days_passed (int): Number of days passed
    
    Returns:
    float: Remaining balance rounded to 2 decimal places
    """
    
    # No decay for first 7 days
    if days_passed <= 7:
        return round(amount, 2)
    
    # Decay starts from day 8
    decay_days = days_passed - 7
    
    # Apply 10% daily decay
    remaining = amount * (0.9 ** decay_days)
    
    return round(remaining, 2)


# Example usage
print(remaining_balance(1000, 5))   # 1000.0
print(remaining_balance(1000, 8))   # 900.0
print(remaining_balance(1000, 10))  # 729.0