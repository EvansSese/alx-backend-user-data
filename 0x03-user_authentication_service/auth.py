#!/usr/bin/env python3
"""Auth module
"""
from bcrypt import hashpw, gensalt
from sqlalchemy.exc import NoResultFound
from db import DB
from user import Base, User


def _hash_password(password: str) -> bytes:
    """FUnction to hash the provided password"""
    hashed = hashpw(password.encode(), gensalt())
    return hashed


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        self._db = DB()
