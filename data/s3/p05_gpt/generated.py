def remaining_balance(starting_amount, days_passed):
    """
    Calculates the remaining cafeteria balance after decay.

    Rules:
    - No decay for the first 7 days
    - Starting from day 8, balance loses 10% each day
    """

    if days_passed <= 7:
        return round(starting_amount, 2)

    decay_days = days_passed - 7

    remaining = starting_amount * (0.9 ** decay_days)

    return round(remaining, 2)


# Example usage
print(remaining_balance(100, 5))   # 100.00
print(remaining_balance(100, 8))   # 90.00
print(remaining_balance(100, 10))  # 72.90