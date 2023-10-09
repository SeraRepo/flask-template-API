import jwt
from functools import wraps
from flask import request, jsonify, Blueprint, request
from flask_cors import cross_origin
from models.models import UserModel, db
from werkzeug.security import generate_password_hash
from .util import get_current_user, token_required
from config import SECRET_KEY

user_bp = Blueprint("user", __name__)

@user_bp.route('/user', methods=['get'])
def get_user():
    """
    Function that returns all the users

    Returns:
        json: json containing all the users
    """
    if request.method == 'GET': 
        users = db.session.query(UserModel).all()
        return jsonify({"ReqStatus": "OK", "Users": [user.serialize() for user in users]})

@user_bp.route('/user/<id>', methods=['get'])
def get_user_by_id(id):
    """
    Function that returns an user

    Returns:
        json: status of the request
    """
    if request.method == 'GET':
        user = UserModel.query.filter_by(id=id).first()
        if user:
            return jsonify({"ReqStatus": "OK", "User": user.serialize()})
        else:
            return jsonify({"ReqStatus": "Error", "response": "No user with this ID"})

@user_bp.route('/user', methods = ['post'])
def create_user():
    """
    Function that creates an user

    Return:
        json: Status of the request
    """
    if request.method == 'POST':
        user_data = request.get_json()
        user_mail = user_data['mail']
        username = user_data['username']
        password = user_data['password']

        new_user = UserModel(userMail=user_mail, username=username, password=generate_password_hash(password))
        db.session.add(new_user)
        db.session.commit()
        return jsonify({"ReqStatus": "OK", "Response": "User successfully created.", "User": new_user.serialize()})

@user_bp.route('/user', methods = ['delete'])
@token_required
def delete_user():
    """
    Function that delete an user

    Returns:
        jsn: status of the requests
    """
    if request.method == 'DELETE':
        user = get_current_user(request)
        if user:
            db.session.delete(user)
            db.session.commit()
            return jsonify({"ReqStatus": "OK", "Response": "User successfully deleted"})
        else:
            return jsonify({"ReqStatus": "Error", "Response": "No user with this ID"})
        
@user_bp.route('/user', methods = ['put'])
@token_required
def update_user():
    """
    Function that update the informations of a user
    
    Returns:
        json: new status of the user
    """
    if request.method == 'PUT':
        user = get_current_user(request)
        if user:
            user_data = request.get_json()
            user.userMail = user_data["mail"] 
            user.username = user_data["username"] 
            user.password = generate_password_hash(user_data["password"])
            db.session.commit()

            return jsonify({"ReqStatus": "OK", "Response": "User successfully updated.", "User": user.serialize()})
        else:
            return jsonify({"ReqStatus": "Error", "Response": "No user with this ID"})     

