"""
Custom Jinja filters
https://flask.palletsprojects.com/en/2.0.x/templating/#registering-filters
"""


def hash8(s: str) -> str:
    """
    Scrambles a string. Returns a string containing 8 digits.
    """
    return abs(hash(s)) % (10 ** 8)
