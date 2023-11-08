#!/usr/bin/env python3
"""This module defines class BasicAuth"""
from .auth import Auth
import re


class BasicAuth(Auth):
    """Handles basic authentication"""
    def extract_base64_authorization_header(
            self,
            authorization_header: str) -> str:
        """Retrieves the Base64 part of the Authorization header"""
        if type(authorization_header) == str:
            pattern = r'Basic (?P<token>.+)'
            field_match = re.fullmatch(pattern, authorization_header.strip())
            if field_match is not None:
                return field_match.group('token')
        return None
