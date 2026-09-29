def calculate_credit(amount, days):
    return round(amount * 0.9 ** max(0, days - 7), 2)
