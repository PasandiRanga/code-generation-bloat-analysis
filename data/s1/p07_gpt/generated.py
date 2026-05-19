# Input
zaps = int(input("Enter zaps count: "))
blitzes = int(input("Enter blitzes count: "))

# Calculate points
zap_points = zaps * 7
blitz_points = blitzes * 13

# Double zap points if blitzes are more than zaps
if blitzes > zaps:
    zap_points *= 2

# Total points
total_points = zap_points + blitz_points

# Output
print("Total points =", total_points)