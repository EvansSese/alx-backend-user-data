#!/usr/bin/env python3
"""Session Auth class"""
import uuid
from api.v1.auth.auth import Auth
from models.user import User


class SessionAuth(Auth):
    """Class to hold Session Auth functions"""
    user_id_by_session_id = {}

    def create_session(self, user_id: str = None) -> str:
        """Function to create session id for a user"""
        if user_id is None or not isinstance(user_id, str):
            return None

        session_id = str(uuid.uuid4())
        self.user_id_by_session_id[session_id] = user_id
        return session_id

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """Function to return session_id for a user"""
        if session_id is None or not isinstance(session_id, str):
            return None
        return self.user_id_by_session_id.get(session_id)

    def current_user(self, request=None) -> str:
        """Function to return a user instance based on cookie value"""
        cookie = self.session_cookie(request)
        session_id = self.user_id_for_session_id(cookie)
        user_id = User.get(session_id)
        return user_id

    def destroy_session(self, request=None) -> bool:
        """Function to destroy user session"""
        if request is None:
            return False
        cookie = self.session_cookie(request)
        if not cookie:
            return False
        if not self.user_id_for_session_id(cookie):
            return False
        del self.user_id_by_session_id[cookie]
        return True
