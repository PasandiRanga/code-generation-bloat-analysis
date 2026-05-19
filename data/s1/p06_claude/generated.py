def zorblax_score(zaps: int, blitzes: int) -> int:
    """
    Calculate total Zorblax points for a round.

    Args:
        zaps    : number of zap points (worth 7 each)
        blitzes : number of blitz points (worth 13 each, doubled if blitzes > zaps)

    Returns:
        Total points for the round.
    """
    if zaps < 0 or blitzes < 0:
        raise ValueError("Zaps and blitzes cannot be negative.")

    ZAP_VALUE    = 7
    BLITZ_VALUE  = 13

    zap_points   = zaps * ZAP_VALUE
    blitz_points = blitzes * BLITZ_VALUE

    # Double blitz points if blitz count exceeds zap count
    if blitzes > zaps:
        blitz_points *= 2

    return zap_points + blitz_points


# --- Quick tests ---
if __name__ == "__main__":
    cases = [
        (3, 2, "blitzes NOT doubled (2 < 3)"),
        (2, 3, "blitzes DOUBLED     (3 > 2)"),
        (4, 4, "blitzes NOT doubled (equal)"),
        (0, 5, "only blitzes, doubled"),
        (5, 0, "only zaps"),
    ]

    for zaps, blitzes, note in cases:
        total = zorblax_score(zaps, blitzes)
        print(f"zaps={zaps}, blitzes={blitzes} → {total:>4} pts  [{note}]")