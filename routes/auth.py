from flask import Blueprint, request,jsonify
from models import db, User
from flask_jwt_extended import create_access_token,jwt_required
from extensions import bcrypt


auth = Blueprint('auth', __name__)

@auth.route('/register', methods = ['POST'])
def register():
    data = request.get_json() # receives data and converts it from JSON to a Python dictionary.

    # Extracting individual values from that dictionary data['name'] means — "get the value with key 'name' from the received data"
    name = data.get('name').lower()
    email= data.get('email').lower()
    password = data.get('password').lower()
    mobile = data.get("mobile")

    if not name or not email or not password:
        return jsonify({"Error":"All fields are required"}), 400
    
    existing_user = User.query.filter_by(email =email).first()
    if existing_user:
        return jsonify({"Error":"User already exists"}), 409

    hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')

    try:
        new_user = User(name = name, email = email, password = hashed_password, mobile = mobile)
        db.session.add(new_user)
        db.session.commit()
    
    except Exception as e:
        db.session.rollback()
        return jsonify({"something went wrong"}), 500


    return jsonify({"message":"User has registered successsfully"}), 201

@auth.route('/change_password', methods = ['POST'])
@jwt_required()
def forgot():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')
    new_password = data.get('new_password')

    user = User.query.filter_by(email = email).first()

    if not user:
        return jsonify({'Error':'User Not Found'}), 404
    
    if not bcrypt.check_password_hash(user.password,password):
        return jsonify({'Error':'Old password not matching'}),401


    hashed_password = bcrypt.generate_password_hash(new_password).decode('utf-8')
    user.password = hashed_password

    try:
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return jsonify({'Error':'Something went wrong'}),500
    
    return jsonify({"Message":"Password has been changed successfully"}),200


    

@auth.route('/login', methods = ["POST"])
def login():
    data = request.get_json()
    email = data.get('email').lower()
    password = data.get('password').lower()

    user = User.query.filter_by(email = email).first()

    if not user:
        return jsonify({"Error":"User Not found"}), 404

    if not bcrypt.check_password_hash(user.password, password):
        return jsonify({"Error":"Wrong Password"}), 401

    token = create_access_token(identity=str(user.id))


    return jsonify({"message":"Login Successful",
    'token':token}), 200
