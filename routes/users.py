from flask import Blueprint, request, jsonify
from models import db, User
from flask_jwt_extended import jwt_required,get_jwt_identity

users = Blueprint('users', __name__)

@users.route('/users', methods = ['GET'])
@jwt_required()
def get_details():
    all_users = User.query.all()
    result = [user.to_dict() for user in all_users]
    return jsonify(result),200

@users.route('/users/<int:id>', methods = ['GET'])
@jwt_required()
def get_user(id):
    user= User.query.filter_by(id = id).first()

    if not user:
        return jsonify({'Error':'user details not available'}),404

    return jsonify(user.to_dict()),200

@users.route('/users/<int:id>', methods = ['PUT'])
@jwt_required()
def update_user(id):
    data = request.get_json()
    user = User.query.filter_by(id = id).first()

    if not user:
        return jsonify({'Error':"Details not Found"}), 404

    if data.get('name'):
        user.name = data.get('name')
    if data.get('email'):
        user.email = data.get('email')
    if data.get('password'):
        user.password = data.get('password')

    try:
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return jsonify({"Error":"Something Went Wrong"}), 500
    


    return jsonify({'Message':'Details updated successfully'}), 200


@users.route('/users/<int:id>', methods = ["DELETE"])
@jwt_required()
def delete_user(id):
    user = User.query.filter_by(id = id).first()

    if not user:
        return jsonify({'Error':"Details not Found"}), 404

    try:
        db.session.delete(user)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return jsonify({"Error":"Something Went Wrong"}), 500


    return jsonify({"Message":"User deleted successfully"}),200