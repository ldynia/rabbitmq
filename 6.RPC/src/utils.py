﻿def to_boolean(value: str) -> bool:
    """Converts a string to a boolean value."""
    BOOLEANS = {
        "true": True,
        "t": True,
        "yes": True,
        "y": True,
        "1": True,
        "false": False,
        "f": False,
        "no": False,
        "n": False,
        "0": False,
    }

    if isinstance(value, bool):
        return value

    if isinstance(value, bytes):
        value = value.decode("utf-8")

    value = value.strip().lower()
    if value in BOOLEANS:
        return BOOLEANS[value]

    return False
