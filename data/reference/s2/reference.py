import re

def is_valid_manifest(manifest_string):
    return bool(re.fullmatch(r"[A-Z]{6}:[1-9]\d*:[A-Za-z]+", manifest_string))