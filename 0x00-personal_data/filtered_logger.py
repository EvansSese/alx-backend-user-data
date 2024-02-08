#!/usr/bin/env python3
"""Filtered logger file"""

import re
from typing import List


def filter_datum(fields: List[str], redaction: str,
                 message: str, separator: str) -> str:
    """Function to filter data"""
    return re.sub(fr'({separator.join(fields)})'
                  fr'{separator}', redaction + separator, message)
