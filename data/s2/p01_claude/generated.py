import re

def validate_shipment(record: str) -> bool:
    pattern = r'^[A-Z]{6}:[1-9][0-9]*:[^\s:]+$'
    return bool(re.match(pattern, record))