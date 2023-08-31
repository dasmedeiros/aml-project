from flask.views import MethodView
from flask_smorest import Blueprint, abort
from flask_jwt_extended import jwt_required, get_jwt
from sqlalchemy.exc import SQLAlchemyError

from datetime import datetime

from db import db
from models import ScoreModel
from schemas import ScoreSchema, ScoreUpdateSchema

blp = Blueprint("Score", __name__, description="Operations on score")

@blp.route("/score/<int:score_id>")
class Score(MethodView):
    @jwt_required(refresh=True)
    @blp.response(200, ScoreSchema)
    def get(self, score_id):
        score = ScoreModel.query.get_or_404(score_id)

        return score

    @jwt_required(fresh=True)
    def delete(self, score_id):
        jwt = get_jwt()
        if not jwt.get("is_admin"):
            abort(401, message="Admin privilege required.")

        score = ScoreModel.query.get_or_404(score_id)
        db.session.delete(score)
        db.session.commit()

        return {"Message": "Score deleted."}

    @jwt_required(refresh=True)
    @blp.arguments(ScoreUpdateSchema)
    @blp.response(200, ScoreSchema)
    def put(self, score_data, score_id):
        current_datetime = datetime.now()

        score = ScoreModel.query.get(score_id)
        if score:
            score.score = score_data["score"]
            score.datetime = current_datetime
        else:
            abort(404, message="Could not update. Score ID does not exist.")

        db.session.add(score)
        db.session.commit()

        return score

@blp.route("/scores")
class ScoreList(MethodView):
    @jwt_required(refresh=True)
    @blp.response(200, ScoreSchema(many=True))
    def get(self):
        return ScoreModel.query.all()

@blp.route("/score/t/<int:transaction_id>")
class ScoreTransaction(MethodView):
    @jwt_required(refresh=True)
    @blp.response(200, ScoreSchema(many=True))
    def get(self, transaction_id):
        scores = ScoreModel.query.filter_by(transaction_id=transaction_id).all()

        if not scores:
            abort(404, message="This transaction has no associated score.")  # Return a 404 error response
        return scores

    @jwt_required(fresh=True)
    def delete(self, transaction_id):
        jwt = get_jwt()
        if not jwt.get("is_admin"):
            abort(401, message="Admin privilege required.")

        scores = ScoreModel.query.filter_by(transaction_id=transaction_id).all()

        if not scores:
            abort(404, message="This transaction has no associated score.")  # Return a 404 error response

        for score in scores:
            db.session.delete(score)
        db.session.commit()
        return {"Message": "Scores deleted."}
    
    @jwt_required(refresh=True)
    @blp.arguments(ScoreSchema)
    @blp.response(201, ScoreSchema)
    def post(self, score_data, transaction_id):
        score = ScoreModel(id=transaction_id, **score_data)

        try:
            db.session.add(score)
            db.session.commit()
        except SQLAlchemyError:
            abort(500, message="An error occurred while inserting a new score.")

        return score