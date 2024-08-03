import re

from Dmhylib import log

pat = re.compile(r'(\d+(?:\.\d+)?)\s*(\w+)')

conversion_factors = {
    'B': 1,
    'KB': 1024,
    'MB': 1048576,
    'GB': 1073741824,
    'TB': 1099511627776
}


def convert_byte(value, from_unit, to_unit):
    if from_unit not in conversion_factors or to_unit not in conversion_factors:
        log.critical("This error may mean that the program has not worked as expected:")
        raise ValueError(f"Convert: invalid storage unit '{from_unit}'")

    from_factor = conversion_factors[from_unit]
    to_factor = conversion_factors[to_unit]
    return round(value * (from_factor / to_factor), 2)


def extract_value_and_unit(size):
    match = pat.match(size)

    if match:
        value = float(match.group(1))
        unit = match.group(2)
        return value, unit
    else:
        log.critical("This error may mean that the program has not worked as expected:")
        raise ValueError(f"Extract: invalid size '{size}'")
