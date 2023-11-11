#!/usr/bin/env python3
"""This moduled defines class SessionExpAuth"""
from api.v1.auth.session_auth import SessionAuth
from uuid import uuid4
from os import getenv
from models.user import User
from datetime import datetime, timedelta


class SessionExpAuth(SessionAuth):
    """Handles Session Authentication Expiration"""
    user_id_by_session_id = {}

    def __init__(self):
        """Initialization"""
        super().__init__()
        session_duration = getenv('SESSION_DURATION')
        if not session_duration:
            self.session_duration = 0
        try:
            self.session_duration = int(session_duration)
        except ValueError:
            self.session_duration = 0

    def create_session(self, user_id=None):
        """create a session"""
        session_id = super().create_session(user_id)
        if not session_id:
            return None
        session_dict = {'user_id': user_id, 'created_at': datetime.now()}
        self.user_id_by_session_id[session_id] = session_dict
        return session_id

    def user_id_for_session_id(self, session_id=None):
        """user id for session id"""
        if not session_id:
            return None
        user_dict = self.user_id_by_session_id.get(session_id)
        if not user_dict:
            return None
        if self.session_duration <= 0:
            return user_dict.get('user_id')
        if not user_dict.get('created_at'):
            return None
        duration = timedelta(seconds=self.session_duration)
        expiration = user_dict.get('created_at') + duration
        if expiration < datetime.now():
            return None
        return user_dict.get('user_id')
