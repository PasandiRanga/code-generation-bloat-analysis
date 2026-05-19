def calculate_score():
    total_score = 0
    round_number = 1

    while True:
        print(f"\n--- Round {round_number} ---")
        
        zaps = int(input("Enter number of Zaps: "))
        blitzes = int(input("Enter number of Blitzes: "))

        # Stop condition
        if zaps == 0 and blitzes == 0:
            print("\nGame Over!")
            break

        # Base points
        zap_points = zaps * 7
        blitz_points = blitzes * 13

        # Special condition (only in first round)
        if round_number == 1 and blitzes > zaps:
            zap_points *= 2
            print("Special bonus applied! Zap points doubled.")

        round_score = zap_points + blitz_points
        total_score += round_score

        print(f"Round {round_number} Score: {round_score}")
        print(f"Total Score so far: {total_score}")

        round_number += 1

    print(f"\nFinal Score: {total_score}")


# Run the game
calculate_score()