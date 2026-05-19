def is_valid_cargo(record):
    # Split by colon
    parts = record.split(":")
    
    # Must have exactly 3 parts
    if len(parts) != 3:
        return False
    
    ship_id, weight, destination = parts
    
    # SHIPID: exactly 6 uppercase letters
    if len(ship_id) != 6 or not ship_id.isalpha() or not ship_id.isupper():
        return False
    
    # WEIGHT: positive whole number
    if not weight.isdigit() or int(weight) <= 0:
        return False
    
    # DESTINATION: single word (no spaces)
    if " " in destination or destination == "":
        return False
    
    return True