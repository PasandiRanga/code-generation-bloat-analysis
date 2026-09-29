def final_score(zaps, blitzes):
    return zaps * (14 if blitzes > zaps else 7) + blitzes * 13
