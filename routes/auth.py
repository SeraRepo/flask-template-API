import jwt
from functools import wraps
from flask import request, jsonify, Blueprint, request
from flask_cors import cross_origin
from models.models import UserModel, db
from werkzeug.security import check_password_hash
from datetime import datetime, timedelta
from .util import get_current_user, token_required
from config import SECRET_KEY

auth_bp = Blueprint("auth", __name__)

@auth_bp.route('/login', methods = ['post'])
def login():
    """
    Function that log an user

    Returns:
        json: Status of the request
    """

    if request.method == 'POST':
        credentials = request.get_json()
        username = credentials["username"]
        password = credentials["password"]

        user = UserModel.query.filter_by(username=username).first()
        
        if user:
            if check_password_hash(user.password, password):
                token = jwt.encode({
                    'id': user.id,
                    'exp' : datetime.utcnow() + timedelta(minutes = 30)
                    }, SECRET_KEY)
                user.jwt = token.decode('UTF-8') 
                db.session.commit()
                return jsonify({"ReqStatus": "OK", "Response": "User logged in.", "JWT": user.jwt })
            else:
                return jsonify({"ReqStatus": "KO", "Response": "Invalid Credentials."})
        else:
            return jsonify({"ReqStatus": "KO", "Response": "Invalid Credentials."})
        
@auth_bp.route('/logout', methods = ['post'])
@token_required
def logout():
    """
    Function that log out the current user

    Returns:
        json: Status of the requests
    """
    if request.method == 'POST':
        user = get_current_user(request)
        if user:
            user.jwt = None
            db.session.commit()
            return jsonify({"ReqStatus": "OK", "Response": "User successfully log out."})
