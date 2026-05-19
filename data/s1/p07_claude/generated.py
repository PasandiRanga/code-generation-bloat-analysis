def zorblax_points(zaps, blitzes):
    zap_points = zaps * 7
    blitz_points = blitzes * 13
    
    if blitzes > zaps:
        zap_points *= 2
    
    return zap_points + blitz_points


# Example usage
zaps = int(input("Enter zaps count: "))
blitzes = int(input("Enter blitzes count: "))

total = zorblax_points(zaps, blitzes)
print(f"Total points: {total}")