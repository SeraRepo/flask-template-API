import jwt
from functools import wraps
from flask import request, jsonify, request
from models.models import UserModel, db
from config import SECRET_KEY

def get_current_user(request):
    """
    Get the user that send the request

    Args:
        request: Request sent by the user

    Returns:
        string: Id of the user
    """
    token = request.headers['x-access-token']
    data = jwt.decode(token, SECRET_KEY,algorithm=["HS256"])
    user = UserModel.query.filter_by(id = data['id']).first()
    return user

def token_required(f):
    """
    Function that raise an error if the token sent by the user is not the same as the token of the resource he seeks to get
    """
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None

        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token']
        if not token:
            return jsonify({"ReqStatus": "KO", 'message' : 'Token is missing !!'}), 401

        try:
            data = jwt.decode(token, SECRET_KEY)
        except Exception as e:
            return jsonify({"ReqStatus": "KO", "Response": "Error token"}), 401

        current_user = UserModel.query.filter_by(id = data['id']).first()
        ctoken = current_user.jwt

        if token != ctoken:
            return jsonify({"ReqStatus": "KO", "Response": "Error token"}), 401
        if token == "":
            return jsonify({"ReqStatus": "KO", "Response": "Error token"}), 401

        return  f(*args, **kwargs)
    return decorated