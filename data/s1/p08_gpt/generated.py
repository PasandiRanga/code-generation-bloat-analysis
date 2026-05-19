def calculate_score(x, y):
    zap_score = 7 * x
    blitz_score = 13 * y

    # SP combo rule
    if y > x:
        zap_score *= 2

    total_score = zap_score + blitz_score
    return total_score