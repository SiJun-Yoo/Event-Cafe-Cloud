import jwt
from flask import request, render_template, Blueprint, jsonify

from database import DB
from controller.auth_controller import SECRET_KEY


class ECTOKEN:
    def get_token(object):
        token = request.cookies.get("jwt_token")
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
            user = DB.find_one("users", {"user_id": payload["user_id"]}, {"_id": False})
            return user
        except (jwt.ExpiredSignatureError, jwt.exceptions.DecodeError):
            return None

    def get_user_id(object):
        token = request.cookies.get("jwt_token")
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
            user_id = payload["user_id"]
            return user_id
        except (jwt.ExpiredSignatureError, jwt.exceptions.DecodeError):
            return None
