def validate_record(record):
    # Split the record using colon
    parts = record.split(":")

    # Rule 1: Must contain exactly 3 parts
    if len(parts) != 3:
        return False

    shipid, weight, destination = parts

    # Rule 2: SHIPID must be 6 uppercase letters
    if not (len(shipid) == 6 and shipid.isalpha() and shipid.isupper()):
        return False

    # Rule 3: WEIGHT must be a positive whole number
    if not (weight.isdigit() and int(weight) > 0):
        return False

    # Rule 4: DESTINATION must be a single word without spaces
    if " " in destination or destination == "":
        return False

    return True


# Example usage
print(validate_record("ABCDEF:120:Mars"))       # True
print(validate_record("ABC12F:120:Mars"))       # False
print(validate_record("abcdef:120:Mars"))       # False
print(validate_record("ABCDEF:-50:Mars"))       # False
print(validate_record("ABCDEF:120:New York"))   # False