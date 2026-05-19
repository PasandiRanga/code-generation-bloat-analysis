import re

def is_valid_cargo(record: str) -> bool:
    """
    Validates a cargo record string.
    
    Format: SHIPID:WEIGHT:DESTINATION
    - SHIPID: exactly 6 uppercase letters
    - WEIGHT: whole number greater than 0
    - DESTINATION: a single word with no spaces
    """
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