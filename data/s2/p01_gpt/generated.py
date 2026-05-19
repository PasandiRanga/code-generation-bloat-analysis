def is_valid_record(record):
    parts = record.split(":")

    # Must have exactly 3 parts
    if len(parts) != 3:
        return False

    shipid, weight, destination = parts

    # Check SHIPID: exactly 6 uppercase letters
    if not (len(shipid) == 6 and shipid.isalpha() and shipid.isupper()):
        return False

    # Check WEIGHT: positive integer
    if not (weight.isdigit() and int(weight) > 0):
        return False

    # Check DESTINATION: no spaces and not empty
    if not (destination and " " not in destination):
        return False

    return True