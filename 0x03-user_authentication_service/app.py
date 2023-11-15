#!/usr/bin/env python3
"""This module defines a basic flask app"""
from flask import Flask
from flask import jsonify, request, abort, make_response, redirect, url_for
from auth import Auth

app = Flask(__name__)
AUTH = Auth()


@app.route('/', strict_slashes=False)
def home():
    """home page"""
    return jsonify({"message": "Bienvenue"})


@app.route('/users', methods=['POST'], strict_slashes=False)
def users():
    """register user"""
    # retrieve data from users via form
    data = request.form.to_dict()
    try:
        email = data.get('email')
        password = data.get('password')
        user = AUTH.register_user(email, password)
    except ValueError:
        return jsonify({"message": "email already registered"}), 400

    return jsonify({"email": user.email, "message": "user created"})


@app.route('/sessions', methods=['POST'], strict_slashes=False)
def login():
    """login page"""
    data = request.form.to_dict()
    email = data.get('email')
    password = data.get('password')

    # verify login credentials
    user_valid = AUTH.valid_login(email, password)

    if user_valid:
        # create a session for this user
        session_id = AUTH.create_session(email)
        payload = {"email": email, "message": "logged in"}
        response = make_response(jsonify(payload))
        # create cookie and attach it before response return
        response.set_cookie('session_id', session_id)
        return response
    else:
        abort(401)


@app.route('/sessions', methods=['DELETE'], strict_slashes=False)
def logout():
    """logout"""
    # use cookie to get session id
    session_id = request.cookies.get('session_id')
    user = AUTH.get_user_from_session_id(session_id)
    if user:
        AUTH.destroy_session(user.id)
        return redirect(url_for('home'))
    else:
        abort(403)


@app.route('/profile', methods=['GET'], strict_slashes=False)
def profile():
    """returns user's profile (email)"""
    session_id = request.cookies.get('session_id')
    user = AUTH.get_user_from_session_id(session_id)
    if user:
        return jsonify({"email": user.email}), 200
    else:
        abort(403)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
