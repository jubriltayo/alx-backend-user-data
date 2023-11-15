#!/usr/bin/env python3
"""
Main file
"""
import requests

base_url = 'http://127.0.0.1:5000'


def register_user(email: str, password: str) -> None:
    """register user"""
    # expected outputs
    status_code = 200
    payload = {"email": email, "message": "user created"}
    # test
    url = base_url + '/users'
    data = {"email": email, "password": password}
    response = requests.post(url, data)
    assert response.status_code == status_code
    assert response.json() == payload


def log_in_wrong_password(email: str, password: str) -> None:
    """login with wrong password"""
    # expected output
    status_code = 401
    # test
    url = base_url + '/sessions'
    data = {"email": email, "password": password}
    response = requests.post(url, data)
    assert response.status_code == status_code


def log_in(email: str, password: str) -> str:
    """login"""
    # expected outputs
    status_code = 200
    payload = {"email": email, "message": "logged in"}
    # test
    url = base_url + '/sessions'
    data = {"email": email, "password": password}
    response = requests.post(url, data)
    assert response.status_code == status_code
    assert response.json() == payload
    return response.cookies.session_id


def profile_unlogged() -> None:
    """profile unlogged"""
    # expected output
    status_code = 200
    # test
    url = base_url + '/profile'
    response = requests.get(url)
    assert response.status_code == status_code


def profile_logged(session_id: str) -> None:
    """profile logged"""
    # expected outputs
    status_code = 200
    payload = {"email": email}
    # test
    url = base_url + '/profile'
    data = {"session_id": session_id}
    response = requests.get(url, data)
    assert response.status_code == status_code
    assert response.json() == payload


def log_out(session_id: str) -> None:
    """logout"""
    # expected output
    status_code = 200
    # test
    url = base_url + '/sessions'
    data = {"session_id": session_id}
    response = requests.delete(url, data)
    assert response.status_code == status_code


def reset_password_token(email: str) -> str:
    """reset password"""
    # expected output
    status_code = 200
    # test
    url = base_url + '/reset_password'
    data = {"email": email}
    res = requests.post(url, data)
    response = res.json()
    assert res.status_code == status_code
    assert hasattr(response, 'email')
    assert hasattr(response, 'reset_token')
    return response.get('reset token')


def update_password(email: str, reset_token: str, new_password: str) -> None:
    """update password"""
    # expected outputs
    status_code = 200
    payload = {"email": email, "message": "Password updated"}
    # test
    url = base_url + '/reset_password'
    data = {"email": email, 'reset_token': reset_token,
            "new_password": new_password}
    response = requests.put(url, data)
    assert response.status_code == status_code
    assert response.json() == payload


EMAIL = "guillaume@holberton.io"
PASSWD = "b4l0u"
NEW_PASSWD = "t4rt1fl3tt3"


if __name__ == "__main__":

    register_user(EMAIL, PASSWD)
    log_in_wrong_password(EMAIL, NEW_PASSWD)
    profile_unlogged()
    session_id = log_in(EMAIL, PASSWD)
    profile_logged(session_id)
    log_out(session_id)
    reset_token = reset_password_token(EMAIL)
    update_password(EMAIL, reset_token, NEW_PASSWD)
    log_in(EMAIL, NEW_PASSWD)
