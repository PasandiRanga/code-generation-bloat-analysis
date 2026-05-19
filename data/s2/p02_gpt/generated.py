def is_valid_shipment(record):
    parts = record.split(":")

    # Must contain exactly 3 parts
    if len(parts) != 3:
        return False

    shipid, weight, destination = parts

    # SHIPID: exactly 6 uppercase letters
    if not (len(shipid) == 6 and shipid.isalpha() and shipid.isupper()):
        return False

    # WEIGHT: positive whole number
    if not (weight.isdigit() and int(weight) > 0):
        return False

    # DESTINATION: single word without spaces
    if not destination or " " in destination:
        return False

    return True


# Example usage
print(is_valid_shipment("ABCDEF:250:Colombo"))   # True
print(is_valid_shipment("AB12EF:250:Colombo"))   # False
print(is_valid_shipment("ABCDEF:-50:Colombo"))   # False
print(is_valid_shipment("ABCDEF:250:New York"))  # False