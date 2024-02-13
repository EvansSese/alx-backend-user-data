#!/usr/bin/env python3
"""Auth class for Basic authentication"""
from typing import List
from typing_extensions import TypeVar
from flask import request


class Auth:
    """
    Auth class to define auth functions
    """

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """
        Function to check if auth is required
        """
        return False

    def authorization_header(self, request=None) -> str:
        """
        Function to retrurn auth headers
        """
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """Function to return the current user"""
        return None
