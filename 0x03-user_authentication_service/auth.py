#!/usr/bin/env python3
"""Auth module
"""
from bcrypt import hashpw, gensalt, checkpw
from uuid import uuid4
from sqlalchemy.orm.exc import NoResultFound
from db import DB
from user import User


def _hash_password(password: str) -> bytes:
    """FUnction to hash the provided password"""
    hashed = hashpw(password.encode('utf-8'), gensalt())
    return hashed


def _generate_uuid() -> str:
    """Generates a string rep of uuid"""
    return str(uuid4())


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
            user = self._db.add_user(email, hashed_password)
        else:
            raise ValueError(f'User {email} already exists')

        return user

    def valid_login(self, email: str, password: str) -> bool:
        """Check if the provided credentials are correct"""
        try:
            user = self._db.find_user_by(email=email)
        except NoResultFound:
            return False

        user_password = user.hashed_password
        provided_password = password.encode('utf-8')

        if checkpw(provided_password, user_password):
            return True

        return False

    def create_session(self, email: str) -> str:
        """Creates a session id for a logged-in user"""
        try:
            user = self._db.find_user_by(email=email)
            user_session_id = str(_generate_uuid())
            try:
                self._db.update_user(user.id, session_id=user_session_id)
                return user_session_id
            except ValueError:
                pass
        except NoResultFound:
            pass

    def get_user_from_session_id(self, session_id: str) -> User:
        """Get the user from session id"""
        if session_id is None:
            return None
        try:
            user = self._db.find_user_by(session_id=session_id)
            return user
        except NoResultFound:
            return None

    def destroy_session(self, user_id: int) -> None:
        """Destroys a user's session"""
        try:
            user = self._db.find_user_by(id=user_id)
            self._db.update_user(user.id, session_id=None)
        except NoResultFound:
            return None
