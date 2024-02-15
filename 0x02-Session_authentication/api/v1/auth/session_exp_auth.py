#!/usr/bin/env python3
"""Session auth class with expiration"""
from os import getenv
from datetime import datetime, timedelta
from api.v1.auth.session_auth import SessionAuth


class SessionExpAuth(SessionAuth):
    """Session auth class with expiration"""
    def __init__(self):
        """Init method for this class"""
        try:
            duration = int(getenv("SESSION_DURATION"))
        except Exception:
            duration = 0
        self.session_duration = duration

    def create_session(self, user_id=None):
        """Function to create session"""
        try:
            session_id = super().create_session(user_id)
        except Exception:
            return None

        if session_id is None:
            return None
        session_dictionary = {'user_id': user_id, 'created_at': datetime.now()}
        super().user_id_by_session_id[session_id] = session_dictionary
        return session_id

    def user_id_for_session_id(self, session_id=None):
        """Function to get user session id"""
        if session_id is None:
            return None
        if session_id not in super().user_id_by_session_id.keys():
            return None
        session_dictionary = super().user_id_by_session_id[session_id]
        if self.session_duration <= 0:
            return session_dictionary["user_id"]
        if "created_at" not in session_dictionary.keys():
            return None
        create_time = session_dictionary["created_at"]
        time_delta = timedelta(seconds=self.session_duration)
        if (create_time + time_delta) < datetime.now():
            return None
        return session_dictionary["user_id"]

