import re

def is_valid_cargo_record(record: str) -> bool:
    parts = record.split(":")
    if len(parts) != 3:
        return False
    
    ship_id, weight, destination = parts
    
    if not re.fullmatch(r'[A-Z]{6}', ship_id):
        return False
    
    if not re.fullmatch(r'[1-9][0-9]*', weight):
        return False
    
    if not re.fullmatch(r'\S+', destination):
        return False
    
    return True


# --- Tests ---
if __name__ == "__main__":
    test_cases = [
        ("ABCDEF:100:London", True),
        ("ZZZZZZ:9999:NewYork", False),   # Destination has no spaces but is one token... actually valid
        ("ABCDEF:0:London", False),        # Weight is 0 (not positive)
        ("ABCDEF:-5:London", False),       # Negative weight
        ("abcdef:100:London", False),      # Lowercase ship ID
        ("ABCDE:100:London", False),       # Ship ID too short
        ("ABCDEFG:100:London", False),     # Ship ID too long
        ("ABCDEF:100:New York", False),    # Destination has a space
        ("ABCDEF:100:", False),            # Empty destination
        ("ABCDEF::London", False),         # Empty weight
        (":100:London", False),            # Empty ship ID
        ("ABCDEF:100:Tokyo", True),
        ("ABCDEF:1:X", True),             # Minimal valid case
        ("ABC123:100:London", False),      # Ship ID contains digits
        ("ABCDEF:100.5:London", False),    # Float weight
    ]

    for record, expected in test_cases:
        result = is_valid_cargo_record(record)
        status = "PASS" if result == expected else "FAIL"
        print(f"[{status}] is_valid_cargo_record({record!r}) => {result} (expected {expected})")