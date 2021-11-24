"""
Helper functions
"""

from typing import Dict


def all_values_blank(d: Dict) -> bool:
    for key, value in d.items():
        if value:
            return False
    return True


def replace_empty_with_none(d: Dict) -> Dict:
    """
    Replace empty strings with None
    """
    new = {}
    for key, value in d.items():
        if value == '':
            new[key] = None
        else:
            new[key] = value

    return new
