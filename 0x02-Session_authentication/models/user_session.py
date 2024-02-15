#!/usr/bin/env python3
"""User Session class to handle session storage"""
from models.base import Base


class UserSession(Base):
    """User Session class to handle session storage"""
    def __init__(self, *args: list, **kwargs: dict):
        """ Initializes UserSession """
        super().__init__(*args, **kwargs)
        self.user_id = kwargs.get('user_id')
        self.session_id = kwargs.get('session_id')
