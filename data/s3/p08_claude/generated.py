def money_left(M: float, D: int) -> float:
    if D <= 7:
        return round(M, 2)
    
    for _ in range(D - 7):
        M *= 0.9
    
    return round(M, 2)