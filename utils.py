from functools import wraps
from flask_jwt_extended import get_jwt_identity
from models import User
from flask import jsonify

def admin_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        user_id = get_jwt_identity()
        user = User.query.filter_by(id = user_id).first()

        if not user or user.role.lower() != 'admin':
            return jsonify({'Error':' Admin access required'}), 403

        return fn(*args,**kwargs)

    return wrapper

