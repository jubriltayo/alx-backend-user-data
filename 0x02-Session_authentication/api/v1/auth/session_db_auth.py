#!/usr/bin/env python3
"""This moduled defines class SessionDBAuth"""
from api.v1.auth.session_exp_auth import SessionExpAuth
from models.user_session import UserSession


class SessionDBAuth(SessionExpAuth):
    """Session DB Authentication"""
    def create_session(self, user_id=None):
        """ creates a session with persistency in database"""
        session_id = super().create_session(user_id)
        if session_id:
            session = UserSession()
            session.user_id = user_id
            session.session_id = session_id
            session.save()
            return session.id
        return null

    def user_id_for_session_id(self, session_id=None):
        """user id for session id"""
        sessions = UserSession()
        sessions.load_from_file()
        user_session = sessions.get(session_id)
        if user_session:
            return user_session.user_id
        return None

    def destroy_session(self, request=None):
        """destroy session"""
        session_id = self.session_cookie(request)
        u_session = UserSession()
        super().destroy_session()
        u_session.remove(session_id)
