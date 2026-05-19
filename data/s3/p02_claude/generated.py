def calculate_balance(days: int, amount: float) -> float:
    """
    Calculate the balance of digital money after a given number of days.
    
    - For the first 7 days: balance remains unchanged.
    - From day 8 onwards: 10% of the initial amount is deducted each day.
    
    Args:
        days: Number of days elapsed.
        amount: Initial amount of digital money.
    
    Returns:
        Balance rounded to 2 decimal places.
    """
    if days <= 7:
        balance = amount
    else:
        days_of_deduction = days - 7
        total_deduction = days_of_deduction * (0.10 * amount)
        balance = amount - total_deduction

    return round(max(balance, 0), 2)  # Balance can't go below 0