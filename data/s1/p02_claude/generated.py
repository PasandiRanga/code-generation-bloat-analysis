def calculate_zorblax_score(zaps: int, blitzes: int) -> int:
    zap_points = 7
    blitz_points = 13

    if blitzes > zaps:
        zap_points *= 2  # Double points for zaps when blitzes exceed zaps

    return (zaps * zap_points) + (blitzes * blitz_points)