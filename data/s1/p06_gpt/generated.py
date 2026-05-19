def calculate_points(zaps, blitzes):
    zap_points = zaps * 7

    # Double blitz points if blitz count is greater than zaps
    if blitzes > zaps:
        blitz_points = blitzes * 13 * 2
    else:
        blitz_points = blitzes * 13

    total_points = zap_points + blitz_points
    return total_points


# Example usage
print(calculate_points(3, 5))  # Output: 151