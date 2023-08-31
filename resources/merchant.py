from flask.views import MethodView
from flask_smorest import Blueprint, abort
from flask_jwt_extended import jwt_required, get_jwt
from sqlalchemy.exc import SQLAlchemyError

from db import db
from models import MerchantModel
from schemas import MerchantSchema, MerchantUpdateSchema

blp = Blueprint("Merchants", __name__, description="Operations on merchants")

@blp.route("/merchant/<int:merchant_id>")
class Merchant(MethodView):
    @jwt_required(refresh=True)
    @blp.response(200, MerchantSchema)
    def get(self, customer_id):
        merchant = MerchantModel.query.get_or_404(merchant_id)

        return merchant

    @jwt_required(fresh=True)
    def delete(self, merchant_id):
        jwt = get_jwt()
        if not jwt.get("is_admin"):
            abort(401, message="Admin privilege required.")
        
        merchant = MerchantModel.query.get_or_404(merchant_id)
        db.session.delete(merchant)
        db.session.commit()

        return {"Message": "Merchant deleted."}

    @jwt_required(refresh=True)
    @blp.arguments(MerchantUpdateSchema)
    @blp.response(200, MerchantSchema)
    def put(self, merchant_data, merchant_id):
        merchant = MerchantModel.query.get(merchant_id)
        if merchant:
            for key, value in merchant_data.items():
                setattr(merchant, key, value)
        else:
            merchant = MerchantModel(id=merchant_id, **merchant_data)

        db.session.add(merchant)
        db.session.commit()

        return merchant

@blp.route("/merchants")
class MerchantList(MethodView):
    @jwt_required(refresh=True)
    @blp.response(200, MerchantSchema(many=True))
    def get(self):
        return MerchantModel.query.all()

    @jwt_required(refresh=True)
    @blp.arguments(MerchantSchema)
    @blp.response(201, MerchantSchema)
    def post(self, merchant_data):
        jwt = get_jwt()
        if not jwt.get("is_admin"):
            abort(401, message="Admin privilege required.")
        
        merchant = MerchantModel(**merchant_data)

        try:
            db.session.add(merchant)
            db.session.commit()
        except SQLAlchemyError:
            abort(500, message="An error occurred while inserting a new merchant.")

        return merchant
