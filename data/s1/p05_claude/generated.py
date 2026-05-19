def calculate_zorblax_score(zaps: int, blitzes: int) -> int:
    zap_points = 7 * zaps
    if blitzes > zaps:
        zap_points *= 2
    blitz_points = 13 * blitzes
    return zap_points + blitz_points