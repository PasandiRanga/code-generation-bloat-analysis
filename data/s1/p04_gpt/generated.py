def calculate_score(zaps, blitzes):
    zap_points = zaps * 7
    blitz_points = blitzes * 13

    # Double zap points if blitzes are greater than zaps
    if blitzes > zaps:
        zap_points *= 2

    return zap_points + blitz_points


# Example
print(calculate_score(3, 5))  # Output: 107