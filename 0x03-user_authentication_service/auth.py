#!/usr/bin/env python3
"""Auth module
"""
import bcrypt
from bcrypt import hashpw, gensalt
from sqlalchemy.orm.exc import NoResultFound
from db import DB
from user import User


def _hash_password(password: str) -> bytes:
    """FUnction to hash the provided password"""
    hashed = hashpw(password.encode(), gensalt())
    return hashed


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        """Init function to create db instance"""
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """FUnction to register user"""
        try:
            user = self._db.find_user_by(email=email)
        except NoResultFound:
            hashed_password = _hash_password(password)
            user = self._db.add_user(email, str(hashed_password))
        else:
            raise ValueError(f'User {email} already exists')

        return user
