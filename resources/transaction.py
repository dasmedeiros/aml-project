#Operations on transactions
#Operations on hypothetical transactions in a few ways: 
#1) POST 1 random transaction: create a random customer, account, or merchant if any is not given 
#2) POST N random transactions: create a random customer, account, or merchant if any is not given
#3) PUT 1 transaction with a score: link score to transaction_id
#   -> everytime a transaction is updated, check if a score_id is associated, if not create it then update
#   -> if there's already a score_id and a score, create a new score_id and update it
#4) PUT N transactions with a score: link score to transactions based on given customer, account, or merchant
#5) DELETE 1 transaction based on transaction_id
#6) DELETE N transactions based on given customer, account, or merchant
#7) GET all transactions
#8) GET 1 transaction based on transaction_id
#9) GET N transactions based on given customer, account, or merchant  

from flask.views import MethodView
from flask_smorest import Blueprint, abort
from flask_jwt_extended import jwt_required
from sqlalchemy.exc import SQLAlchemyError

from datetime import datetime

from db import db
from models import TransactionModel, ScoreModel
from schemas import TransactionSchema, TransactionUpdateSchema

blp = Blueprint("Transaction", __name__, description="Operations on transaction")

@blp.route("/transaction")
class Transaction(MethodView):
    @jwt_required(refresh=True)
    @blp.arguments(TransactionSchema)
    @blp.response(201, TransactionSchema)
    def post(self, transaction_data):
        transaction = TransactionModel(**transaction_data)

        try:
            db.session.add(transaction)
            db.session.commit()

            # Create a corresponding Score entry and associate it with the transaction
            score = ScoreModel(transaction_id=transaction.id)
            db.session.add(score)
            db.session.commit()

            # Update the transaction with the associated score_id
            transaction.score_id = score.id
            db.session.commit()

        except SQLAlchemyError:
            abort(500, message="An error occurred while inserting a new transaction.")

        return transaction