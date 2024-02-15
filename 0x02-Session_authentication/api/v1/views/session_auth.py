#!/usr/bin/env python3
"""View to handle all session authentication"""
from os import getenv
from flask import request, jsonify
from api.v1.views import app_views
from api.v1.views import User


@app_views.route('/auth_session/login', methods=['POST'],
                 strict_slashes=False)
def session_login() -> str:
    """FUnction to handle login route"""
    user_email = request.form.get('email', None)
    user_password = request.form.get('password', None)
    if user_email is None or '':
        return jsonify({"error":"email missing"}), 400
    if user_password is None or '':
        return jsonify({"error":"password missing"}), 400

    is_valid_user = User.search({'email': user_email})
    if not is_valid_user:
        return jsonify({"error":"no user found for this email"}), 404

    valid_user = is_valid_user[0]

    if not valid_user.is_valid_password(user_password):
        return jsonify({"error": "wrong password"}), 401

    from api.v1.app import auth
    session_id = auth.create_session(valid_user.id)
    cookie_response = getenv('SESSION_NAME')
    user_dict = jsonify(is_valid_user.to_json())

    user_dict.set_cookie(cookie_response, session_id)
    return user_dict
