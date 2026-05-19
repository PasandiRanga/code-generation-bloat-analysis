def remaining_money(start_amount, days):
    amount = start_amount

    # Apply decay starting from day 8
    if days > 7:
        decay_days = days - 7
        for _ in range(decay_days):
            amount *= 0.9  # lose 10% each day

    return round(amount, 2)


# Example usage
print(remaining_money(100, 5))   # 100.0
print(remaining_money(100, 8))   # 90.0
print(remaining_money(100, 10))  # 72.9