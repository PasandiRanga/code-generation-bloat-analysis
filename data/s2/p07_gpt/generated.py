def validate_shipment(record):
    parts = record.split("/")

    # Must have exactly 3 parts
    if len(parts) != 3:
        return False

    ship_id, weight, destination = parts

    # Check Ship ID:
    # exactly 6 uppercase letters
    if not (len(ship_id) == 6 and ship_id.isalpha() and ship_id.isupper()):
        return False

    # Check Weight:
    # positive whole number
    if not (weight.isdigit() and int(weight) > 0):
        return False

    # Check Destination:
    # one word with no spaces
    if " " in destination or destination == "":
        return False

    return True


# Example usage
print(validate_shipment("ABCDEF/120/Mars"))      # True
print(validate_shipment("AB12EF/120/Mars"))      # False
print(validate_shipment("ABCDEF/-50/Mars"))      # False
print(validate_shipment("ABCDEF/120/New York"))  # False