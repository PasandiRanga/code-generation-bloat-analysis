def calculate_remaining_money(start_amount, days):
    if days <= 7:
        return round(start_amount, 2)
    
    remaining = start_amount * (0.9 ** (days - 7))
    return round(remaining, 2)