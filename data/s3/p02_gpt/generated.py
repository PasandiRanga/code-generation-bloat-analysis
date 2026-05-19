def calculate_balance(days, amount):
    balance = amount

    # Apply 10% loss of the initial amount starting from day 8
    if days > 7:
        loss_days = days - 7
        balance -= loss_days * (0.10 * amount)

    # Balance should not go below 0
    balance = max(balance, 0)

    return round(balance, 2)