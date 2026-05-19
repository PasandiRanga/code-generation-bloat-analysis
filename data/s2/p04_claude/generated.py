import re

def is_valid_cargo_record(record: str) -> bool:
    """
    Validates a cargo record in the format "SHIPID:WEIGHT:DESTINATION".
    
    Rules:
    - Exactly 3 parts separated by colons
    - Ship ID: exactly 6 uppercase letters
    - Weight: positive whole number (no decimals, no zero)
    - Destination: single word with no spaces
    
    Returns True if valid, False otherwise.
    """
    if not isinstance(record, str):
        return False

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