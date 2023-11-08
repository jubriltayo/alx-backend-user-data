#!/usr/bin/env python3
"""This module defines class BasicAuth"""
from .auth import Auth
import re
import base64
import binascii


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

    def decode_base64_authorization_header(
                self,
                base64_authorization_header: str,
                ) -> str:
            """ Decodes a base64-encoded authorization header """
            if type(base64_authorization_header) == str:
                try:
                    res = base64.b64decode(
                        base64_authorization_header,
                        validate=True,
                    )
                    return res.decode('utf-8')
                except (binascii.Error, UnicodeDecodeError):
                    return None