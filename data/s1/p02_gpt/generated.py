def calculate_zorblax_score(zaps, blitzes):
    # Base points
    zap_points = 7
    blitz_points = 13

    # Double zap points if blitzes are greater than zaps
    if blitzes > zaps:
        zap_points *= 2

    # Calculate total score
    total_score = (zaps * zap_points) + (blitzes * blitz_points)

    return total_score