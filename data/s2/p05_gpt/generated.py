import re

def is_valid_cargo_record(record):
    # Pattern:
    # ^                 -> start of string
    # [A-Z]{6}          -> exactly 6 uppercase letters
    # :                 -> colon separator
    # [1-9]\d*          -> positive whole number
    # :                 -> colon separator
    # \S+               -> single word with no spaces
    # $                 -> end of string
    
    pattern = r'^[A-Z]{6}:[1-9]\d*:\S+$'
    
    return bool(re.fullmatch(pattern, record))


# Example usage
print(is_valid_cargo_record("ABCDEF:150:MARS"))      # True
print(is_valid_cargo_record("AB1234:150:MARS"))      # False
print(is_valid_cargo_record("ABCDEF:-50:MARS"))      # False
print(is_valid_cargo_record("ABCDEF:0:MARS"))        # False
print(is_valid_cargo_record("ABCDEF:150:NEW YORK"))  # False
print(is_valid_cargo_record("ABCDE:150:MARS"))       # False