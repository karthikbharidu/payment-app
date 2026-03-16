from flask import Blueprint, request, jsonify
from models import db, User, Transaction 
from flask_jwt_extended import jwt_required, get_jwt_identity

transactions = Blueprint('transactions', __name__)

@transactions.route('/transactions', methods = ["POST"])
@jwt_required()
def transaction():
    data = request.get_json()
    user_id = data.get('user_id')
    amount = data.get('amount')
    status = data.get('status')

    if not user_id or not status or not amount:
        return jsonify({"Error":"All fields are required"}),400

    if status not in ["Success","Failed","Pending"]:
        return jsonify({"Error":"Invalid Status"}),400
    
    user = User.query.filter_by(id = user_id).first()

    if not user:
        return jsonify({'Error':"Details not Found"}), 404

    try:
        new_transaction = Transaction(user_id = user_id, amount = amount, status = status)
        db.session.add(new_transaction)
        db.session.commit()
    
    except Exception as e:
        db.session.rollback()
        return jsonify({"Error":"Someting went Wrong"}), 500

     

    return jsonify({"message":"Transaction created successfully"}), 201


@transactions.route('/transactions', methods= ["GET"])
@jwt_required()
def get_transactions():
    txns = Transaction.query.all()
    result = [txn.to_dict() for txn in txns]
    return jsonify(result),200

@transactions.route('/transactions/<int:id>', methods = ["GET"])
@jwt_required()
def transaction_id(id):
    txn = Transaction.query.filter_by(id = id).first()

    if not txn:
        return jsonify({"Error":"Details not Found"}), 404

    return jsonify(txn.to_dict()),200

@transactions.route('/transactions/users/<int:user_id>', methods = ["GET"])
@jwt_required()
def trxns_by_userid(user_id):
    user = User.query.filter_by(id = user_id).first()
    
    if not user:
        return jsonify({"Error":"Details not Found"}), 404

    txns = Transaction.query.filter_by(user_id = user_id).all()

    result = [txn.to_dict() for txn in txns]
    return jsonify(result), 200

@transactions.route('/transactions/status/<status>', methods = ["GET"])
@jwt_required()
def txn_by_status(status):
  

    if status not in ['Success','Failed','Pending']:
        return jsonify({'Error':'Status Not Found'}), 404

    txns = Transaction.query.filter_by(status = status).all()


    result = [txn.to_dict() for txn in txns]
    return jsonify(result), 200
    



