import re 

def is_valid_shipment(record: str) -> bool: 
    """ Validates a cargo shipment record. Format: SHIPID:WEIGHT:DESTINATION - SHIPID: exactly 6 uppercase letters (A–Z) - WEIGHT: positive whole number (no leading zeros) - DESTINATION: single word, no spaces """ 
    pattern = r'^[A-Z]{6}:[1-9][0-9]*:[^\s:]+$'
    return bool(re.fullmatch(pattern, record))