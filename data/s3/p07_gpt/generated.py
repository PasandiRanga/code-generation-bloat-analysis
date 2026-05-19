def money_left(amount, days):
    # First 7 days: no reduction
    if days <= 7:
        return round(amount, 2)

    # Days after the first 7 days
    shrink_days = days - 7

    # Reduce 10% per day
    remaining = amount * (0.9 ** shrink_days)

    return round(remaining, 2)


# Example usage
amount = float(input("Enter initial amount: "))
days = int(input("Enter number of days gone: "))

print("Amount left:", money_left(amount, days))