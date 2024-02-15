#!/usr/bin/env python3
"""Auth class for Basic authentication"""
from os import getenv
from typing import List
from typing_extensions import TypeVar
from flask import request


class Auth:
    """
    Auth class to define auth functions
    """
    SESSION_NAME = getenv("SESSION_NAME")

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """
        Function to check if auth is required
        """
        if path is None or excluded_paths is None or excluded_paths == []:
            return True

        len_path = len(path)
        if len_path == 0:
            return True

        slash_path = True if path[len_path - 1] == '/' else False

        tmp_path = path
        if not slash_path:
            tmp_path += '/'

        for exc_path in excluded_paths:
            len_exc = len(exc_path)
            if len_exc == 0:
                continue

            if exc_path[len_exc - 1] != '*':
                if tmp_path == exc_path:
                    return False
            else:
                if exc_path[:-1] == path[:len_exc - 1]:
                    return False

        return True

    def authorization_header(self, request=None) -> str:
        """
        Function to retrurn auth headers
        """
        if request is None:
            return None

        return request.headers.get("Authorization", None)

    def current_user(self, request=None) -> TypeVar('User'):
        """Function to return the current user"""
        return None

    def session_cookie(self, request=None):
        """Function to return cookie value"""
        if request is None:
            return None
        return request.cookies.get(self.SESSION_NAME)
