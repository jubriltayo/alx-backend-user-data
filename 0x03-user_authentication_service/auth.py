#!/usr/bin/env python3
"""This module contains function `_hash_password`"""
import bcrypt


def _hash_password(password: str) -> bytes:
    """return a salted, and hashed password"""
    encoded = password.encode()
    hashed_pw = bcrypt.hashpw(encoded, bcrypt.gensalt())

    return hashed_pw
