#!/usr/bin/env python3
"""Implementation of encrypting passwords"""

import bcrypt


def hash_password(password: str) -> bytes:
    """Hashes a password using salt"""
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
