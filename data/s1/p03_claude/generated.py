def calculate_score(zaps, blitzes):
    zap_points = 7
    blitz_points = 13
    
    if blitzes > zaps:
        zap_points = 14
    
    return (zaps * zap_points) + (blitzes * blitz_points)