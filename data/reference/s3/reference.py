def calculate_credit(amount: float, days: int):
    return "Values cannot be negative" if amount < 0 or days < 0 else round(amount * (0.9 ** max(0, days - 7)), 2)