def play_game():
    print("=== Welcome to the Zap & Blitz Game ===")
    print("Rules:")
    print("  - Each Zap = 7 points")
    print("  - Each Blitz = 13 points")
    print("  - If Blitzes > Zaps in Round 1, Zap points are DOUBLED for all rounds!")
    print("  - Enter 0 for both to end the game.\n")

    total_score = 0
    round_number = 0
    zap_points = 7  # default points per zap

    while True:
        round_number += 1
        print(f"--- Round {round_number} ---")

        # Get zaps input
        while True:
            try:
                zaps = int(input("  Enter number of Zaps : "))
                if zaps < 0:
                    print("  Please enter a non-negative number.")
                    continue
                break
            except ValueError:
                print("  Invalid input. Please enter a whole number.")

        # Get blitzes input
        while True:
            try:
                blitzes = int(input("  Enter number of Blitzes : "))
                if blitzes < 0:
                    print("  Please enter a non-negative number.")
                    continue
                break
            except ValueError:
                print("  Invalid input. Please enter a whole number.")

        # Check for game-ending condition
        if zaps == 0 and blitzes == 0:
            print("\n  No Zaps or Blitzes collected. Game Over!")
            break

        # Apply special rule at Round 1
        if round_number == 1 and blitzes > zaps:
            zap_points = 14
            print("  ⚡ Special Bonus Activated! Blitzes > Zaps in Round 1 — Zap points DOUBLED to 14!")

        # Calculate round score
        round_score = (zaps * zap_points) + (blitzes * 13)
        total_score += round_score

        # Display round summary
        print(f"\n  Zaps    : {zaps} × {zap_points} = {zaps * zap_points} pts")
        print(f"  Blitzes : {blitzes} × 13      = {blitzes * 13} pts")
        print(f"  Round {round_number} Score : {round_score} pts")
        print(f"  ★ Total Score After Round {round_number}: {total_score} pts\n")

    # Final summary
    print("\n=== Game Summary ===")
    print(f"  Total Rounds Played : {round_number - 1}")
    print(f"  Zap Points Used     : {zap_points} per Zap")
    print(f"  🏆 Final Score      : {total_score} pts")
    print("====================")

play_game()