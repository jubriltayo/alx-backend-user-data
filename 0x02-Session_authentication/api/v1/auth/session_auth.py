#!/usr/bin/env python3
"""This module creates the class SessionAuth"""
from .auth import Auth
from uuid import uuid4


class SessionAuth(Auth):
    """Session Authentication"""
    user_id_by_session_id = {}

    def create_session(self, user_id: str = None) -> str:
        """creates session id"""
        if not user_id and type(user_id) != str and user_id is None:
            return None
        session_id = str(uuid4())
        self.user_id_by_session_id[session_id] = user_id
        return session_id
