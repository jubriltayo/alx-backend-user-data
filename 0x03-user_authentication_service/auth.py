#!/usr/bin/env python3
"""This module contains function `_hash_password`"""
import bcrypt
from db import DB
from user import User
from sqlalchemy.orm.exc import NoResultFound
from uuid import uuid4


def _hash_password(password: str) -> bytes:
    """return a salted, and hashed password"""
    encoded = password.encode()
    hashed_pw = bcrypt.hashpw(encoded, bcrypt.gensalt())

    return hashed_pw


def _generate_uuid() -> str:
    """generate random user identifier"""
    return str(uuid4())


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """register user"""
        try:
            user_in_db = self._db.find_user_by(email=email)
            if user_in_db:
                raise ValueError(f"User {email} already exists")
        except NoResultFound:
            hash_pw = _hash_password(password)
            user = self._db.add_user(email, hash_pw)
            return user

    def valid_login(self, email: str, password: str) -> bool:
        """verifies login credentials"""
        try:
            user_in_db = self._db.find_user_by(email=email)
            if user_in_db:
                encoded_pw = password.encode()
                user_pw = user_in_db.hashed_password
                return bcrypt.checkpw(encoded_pw, user_pw)
            return False
        except NoResultFound:
            return False

    def create_session(self, email: str) -> str:
        """create new session with email and returns session id"""
        try:
            user_in_db = self._db.find_user_by(email=email)
            if user_in_db:
                session_id = _generate_uuid()
                self._db.update_user(user_in_db.id, session_id=session_id)
                return session_id
        except Exception:
            return None
