def final_score(z, b):
    if z < 0 or b < 0:
        return "Values cannot be negative"
    return (z * (14 if b > z else 7)) + b * 13