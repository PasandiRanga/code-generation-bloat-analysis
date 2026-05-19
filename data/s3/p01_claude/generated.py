def cafeteria_balance(starting_amount: float, days_passed: int) -> float:
    """
    Calculate remaining cafeteria digital money after decay.

    Rules:
    - Days 1–7: No decay (money is safe)
    - Day 8 onwards: 10% decay per day (compounding on current balance)

    Args:
        starting_amount: The initial amount of digital money issued
        days_passed: The number of days that have passed since issuance

    Returns:
        Remaining balance rounded to 2 decimal places
    """
    if days_passed <= 7:
        return round(starting_amount, 2)

    decay_days = days_passed - 7
    remaining = starting_amount * (0.9 ** decay_days)

    return round(remaining, 2)


# --- Manual Testing ---
if __name__ == "__main__":
    test_cases = [
        (100.00, 0),   # Before any day passes
        (100.00, 7),   # Last safe day — no decay
        (100.00, 8),   # First decay day: -10%
        (100.00, 9),   # Second decay day: -10% of remaining
        (100.00, 17),  # 10 full decay days
        (250.00, 10),  # Custom amount, 3 decay days
    ]

    print(f"{'Start':>10} | {'Days':>5} | {'Remaining':>10}")
    print("-" * 32)
    for amount, days in test_cases:
        result = cafeteria_balance(amount, days)
        print(f"${amount:>9.2f} | {days:>5} | ${result:>9.2f}")