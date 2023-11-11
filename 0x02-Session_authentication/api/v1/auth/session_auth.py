#!/usr/bin/env python3
"""This module creates the class SessionAuth"""
from .auth import Auth
from uuid import uuid4
from models.user import User


class SessionAuth(Auth):
    """Session Authentication"""
    user_id_by_session_id = {}

    def create_session(self, user_id: str = None) -> str:
        """creates session id"""
        if not user_id or type(user_id) != str:
            return None
        session_id = str(uuid4())
        self.user_id_by_session_id[session_id] = user_id
        return session_id

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """returns user id based on session id"""
        if not session_id or type(session_id) != str:
            return None
        return self.user_id_by_session_id.get(session_id)

    def current_user(self, request=None):
        """returns User instance based on cookie value"""
        cookie_value = self.session_cookie(request)
        user_id = self.user_id_for_session_id(cookie_value)
        return User.get(user_id)
