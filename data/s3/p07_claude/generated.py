import math

def cafeteria_money(initial_amount, days):
    if days <= 7:
        return round(initial_amount, 2)
    
    shrink_days = days - 7
    remaining = initial_amount * (0.9 ** shrink_days)
    return round(remaining, 2)

# Input
amount = float(input("Enter initial amount of money: "))
days = int(input("Enter number of days gone: "))

result = cafeteria_money(amount, days)
print(f"Amount of money left: {result}")