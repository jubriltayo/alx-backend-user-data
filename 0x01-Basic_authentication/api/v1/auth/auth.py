#!/usr/bin/env python3
"""This module handles the API authentication"""

from flask import request
from typing import List, TypeVar


class Auth():
    """
    Class for managing API authentication
    """
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """Checks if authentication is required for a given path"""
        if excluded_paths is None or excluded_paths == [] or path is None:
            return True
        else:
            if not path.endswith('/'):
                path = path + '/'
            if path in excluded_paths:
                return False
        return True

    def authorization_header(self, request=None) -> str:
        """Extracts the authorization header from the request"""
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """Returns current user based on request"""
        return None
