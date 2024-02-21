#!/usr/bin/env python3
"""Auth module
"""
from bcrypt import hashpw, gensalt
from sqlalchemy.exc import NoResultFound
from db import DB


def _hash_password(password: str) -> bytes:
    """FUnction to hash the provided password"""
    hashed = hashpw(password.encode(), gensalt())
    return hashed
