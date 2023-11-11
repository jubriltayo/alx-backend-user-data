#!/usr/bin/env python3
"""This module handles views from Session Authentication"""
from api.v1.views import app_views
from flask import jsonify, request
from models.user import User
from os import getenv


@app_views.route('/auth_session/login', methods=['POST'], strict_slashes=False)
def login() -> str:
    """POST /api/v1/auth_session/login
    Return:
      - None
    """
    email = request.form.get('email')
    password = request.form.get('password')
    if not email:
        return jsonify({"error": "email missing"}), 400
    if not password:
        return jsonify({"error": "password missing"}), 400
    users = User.search({'email': email})
    if not users or users == []:
        return jsonify({"error": "no user found for this email"}), 404
    user = users[0]
    valid_password = user.is_valid_password(password)
    if not valid_password:
        return jsonify({"error": "wrong password"}), 401
    from api.v1.app import auth
    session_id = auth.create_session(user.id)
    session_tip = getenv("SESSION_NAME")
    # jsonify returns a Response object,
    # so add cookie with set_cookie before it returns
    response = jsonify(user.to_json())
    response.set_cookie(session_tip, session_id)
    return response
