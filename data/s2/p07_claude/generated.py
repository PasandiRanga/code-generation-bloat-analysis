import re

def validate_shipment(shipment: str) -> bool:
    pattern = r'^[A-Z]{6}/[1-9][0-9]*/\S+$'
    return bool(re.match(pattern, shipment))

# Test cases
test_cases = [
    "ABCDEF/100/Mars",        # True
    "XYZABC/1/Earth",         # True
    "abcdef/100/Mars",        # False - lowercase letters
    "ABCDE/100/Mars",         # False - only 5 letters
    "ABCDEFG/100/Mars",       # False - 7 letters
    "ABCDEF/0/Mars",          # False - weight is 0
    "ABCDEF/-5/Mars",         # False - negative weight
    "ABCDEF/100/",            # False - empty destination
    "ABCDEF/100/New Mars",    # False - space in destination
    "ABCDEF/100.5/Mars",      # False - decimal weight
    "ABCDEF/100",             # False - missing destination
    "/100/Mars",              # False - missing ship ID
]

for test in test_cases:
    result = validate_shipment(test)
    print(f"'{test}' -> {result}")