#!/usr/bin/env python3
"""Filtered logger file"""

import re


def filter_datum(fields, redaction, message, separator):
    """Function to filter data"""
    return re.sub(fr'({separator.join(fields)})'
                  fr'{separator}', redaction + separator, message)
