def is_valid_cargo(record):
    # Split into exactly 3 parts
    parts = record.split(":")
    
    if len(parts) != 3:
        return False

    ship_id, weight, destination = parts

    # Check SHIPID: exactly 6 uppercase letters
    if not (len(ship_id) == 6 and ship_id.isalpha() and ship_id.isupper()):
        return False

    # Check WEIGHT: whole number > 0
    if not (weight.isdigit() and int(weight) > 0):
        return False

    # Check DESTINATION: single word with no spaces
    if not (destination.isalpha() and " " not in destination):
        return False

    return True