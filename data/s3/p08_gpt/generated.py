def money_left(M, D):
    money = float(M)

    # No decay for first 7 days
    if D <= 7:
        return f"{money:.2f}"

    # Apply 10% decay starting from day 8
    decay_days = D - 7

    for _ in range(decay_days):
        money *= 0.9

    return f"{money:.2f}"