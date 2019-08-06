"""Utilities for the led library"""


def clamp(n, min_n, max_n):
    """Limits the range of n between min_n and max_n"""
    return max(min(max_n, n), min_n)

