def calculate_score(zaps, blitzes):
    zap_points = zaps * 7
    blitz_points = blitzes * 13

    # If blitzes are greater than zaps,
    # zap points count double
    if blitzes > zaps:
        zap_points *= 2

    total_score = zap_points + blitz_points
    return total_score