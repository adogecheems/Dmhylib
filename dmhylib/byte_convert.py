import re
from collections import OrderedDict
from typing import Tuple

from dmhylib import log

size_pattern = re.compile(r'(\d+(?:\.\d+)?)\s*(\w+)')

conversion_factors = OrderedDict([
    ('B', 1),
    ('KB', 1024),
    ('MB', 1048576),
    ('GB', 1073741824),
    ('TB', 1099511627776)
])


def convert_byte(value: float, from_unit: str, to_unit: str) -> float:
    """
    Convert a byte value from one unit to another.

    Args:
        value (float): The value to convert.
        from_unit (str): The unit to convert from.
        to_unit (str): The unit to convert to.

    Returns:
        float: The converted value.

    Raises:
        ValueError: If an invalid storage unit is provided.
    """
    try:
        from_factor = conversion_factors[from_unit.upper()]
        to_factor = conversion_factors[to_unit.upper()]
    except KeyError as e:
        log.critical("This error may mean that the program has not worked as expected:")
        raise ValueError(f"Convert: invalid storage unit '{e.args[0]}'") from e

    return round(value * (from_factor / to_factor), 2)


def extract_value_and_unit(size: str) -> Tuple[float, str]:
    """
    Extract the numeric value and unit from a size string.

    Args:
        size (str): The size string to parse.

    Returns:
        Tuple[float, str]: The extracted value and unit.

    Raises:
        ValueError: If the size string is invalid.
    """
    match = size_pattern.match(size)

    if match:
        value = float(match.group(1))
        unit = match.group(2)
        return value, unit
    else:
        log.critical("This error may mean that the program has not worked as expected:")
        raise ValueError(f"Extract: invalid size '{size}'")
