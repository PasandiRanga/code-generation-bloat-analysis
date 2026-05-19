import re

def validate_cargo_record(record: str) -> bool:
    pattern = r'^[A-Z]{6}:\d+:[^\s:]+$'
    
    if not re.match(pattern, record):
        return False
    
    parts = record.split(':')
    weight = int(parts[1])
    
    return weight > 0