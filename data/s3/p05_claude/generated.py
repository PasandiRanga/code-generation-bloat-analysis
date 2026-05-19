def calculate_balance(starting_amount: float, days: int) -> float:
    """
    Calculate remaining cafeteria balance after decay.

    Rules:
      - Days 0–7:  no decay, balance is fully intact
      - Day 8+:   10% lost per day (i.e. balance × 0.9 per day)

    Args:
        starting_amount: The initial amount of digital money.
        days:            Number of days that have passed.

    Returns:
        Remaining balance rounded to 2 decimal places.
    """
    if days <= 7:
        return round(starting_amount, 2)

    decay_days = days - 7                          # days subject to decay
    balance = starting_amount * (0.9 ** decay_days)  # compound 10% daily loss
    return round(balance, 2)