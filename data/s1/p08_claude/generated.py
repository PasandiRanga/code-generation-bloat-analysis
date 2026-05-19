def calculate_score(x, y):
    zap_score = 7 * x
    blitz_score = 13 * y
    
    if y > x:
        zap_score *= 2
    
    return zap_score + blitz_score