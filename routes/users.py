from flask import Blueprint, request, jsonify
from models import db, User,Transaction
from flask_jwt_extended import jwt_required,get_jwt_identity
from utils import admin_required
from extensions import bcrypt

users = Blueprint('users', __name__)

@users.route('/users', methods = ['GET'])
@jwt_required()
@admin_required
def get_details():
    page = request.args.get('page', 1, type = int)
    limit = request.args.get('limit', 10, type = int)
    
    paginated = User.query.paginate(page = page, per_page = limit, error_out = False)
    return jsonify({
        'users':[user.to_dict() for user in paginated.items],
        'total_users': paginated.total,
        'page': paginated.page,
        'total_pages':paginated.pages,
        'has_next': paginated.has_next,
        'has_previous': paginated.has_prev
    }),200

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
    current_user_id = get_jwt_identity()
    current_user = User.query.filter_by(id = current_user_id).first()

    if current_user.role !='admin' and current_user_id !=str(id):
        return jsonify({'Error':'Unauthorized'}), 403


    if not user:
        return jsonify({'Error':"Details not Found"}), 404

    if data.get('name'):
        user.name = data.get('name')
    if data.get('email'):
        user.email = data.get('email')
    if data.get('password'):
        hashed_password = bcrypt.generate_password_hash(data.get('password')).decode('utf-8')
        user.password = hashed_password

    try:
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return jsonify({"Error":"Something Went Wrong"}), 500
    


    return jsonify({'Message':'Details updated successfully'}), 200


@users.route('/users/<int:id>', methods = ["DELETE"])
@jwt_required()
@admin_required
def delete_user(id):
    user = User.query.filter_by(id = id).first()

    if not user:
        return jsonify({'Error':"Details not Found"}), 404

    try:
        Transaction.query.filter_by(user_id = id).delete()
        db.session.delete(user)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        print(f"ERROR: {e}") 
        return jsonify({"Error":"Something Went Wrong"}), 500


    return jsonify({"Message":"User deleted successfully"}),200