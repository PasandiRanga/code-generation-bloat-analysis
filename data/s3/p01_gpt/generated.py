def remaining_money(amount, days):
    # No decay for first 7 days
    if days <= 7:
        return round(amount, 2)
    
    # Number of decay days
    decay_days = days - 7
    
    # Apply 10% decay each day
    final_amount = amount * (0.9 ** decay_days)
    
    return round(final_amount, 2)


# Example usage
amount = float(input("Enter starting amount: "))
days = int(input("Enter number of days: "))

result = remaining_money(amount, days)
print(f"Remaining money: {result:.2f}")