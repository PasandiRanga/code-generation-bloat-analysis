def is_valid_cargo_record(record):
    # Split the record into parts
    parts = record.split(":")

    # Must have exactly 3 parts
    if len(parts) != 3:
        return False

    ship_id, weight, destination = parts

    # SHIPID: exactly 6 uppercase letters
    if not (len(ship_id) == 6 and ship_id.isalpha() and ship_id.isupper()):
        return False

    # WEIGHT: positive whole number
    if not (weight.isdigit() and int(weight) > 0):
        return False

    # DESTINATION: single word without spaces
    if " " in destination or destination == "":
        return False

    return True


# Example tests
print(is_valid_cargo_record("ABCDEF:150:MoonBase"))   # True
print(is_valid_cargo_record("AB123F:150:MoonBase"))   # False
print(is_valid_cargo_record("ABCDEF:-50:MoonBase"))   # False
print(is_valid_cargo_record("ABCDEF:150:Moon Base"))  # False