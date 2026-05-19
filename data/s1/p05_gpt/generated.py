def calculate_zorblax_score(zaps, blitzes):
    # Base points
    zap_points = zaps * 7
    blitz_points = blitzes * 13

    # Special combo rule:
    # If blitzes are strictly greater than zaps,
    # double the points earned from zaps
    if blitzes > zaps:
        zap_points *= 2

    # Total score
    total_score = zap_points + blitz_points

    return total_score
