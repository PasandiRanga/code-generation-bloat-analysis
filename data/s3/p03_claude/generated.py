def calculate_cafeteria_balance(starting_amount: float, days: int) -> float:
    if days <= 7:
        return round(starting_amount, 2)
    
    balance = starting_amount
    decay_days = days - 7
    balance *= (0.9 ** decay_days)
    
    return round(balance, 2)