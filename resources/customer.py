from flask.views import MethodView
from flask_smorest import Blueprint, abort
from flask_jwt_extended import jwt_required
from sqlalchemy.exc import SQLAlchemyError

from db import db
from models import CustomerModel
from schemas import CustomerSchema, CustomerUpdateSchema

blp = Blueprint("Customers", __name__, description="Operations on customers")

@blp.route("/customer/<string:customer_id>")
class Customer(MethodView):
    @jwt_required()
    @blp.response(200, CustomerSchema)
    def get(self, customer_id):
        customer = CustomerModel.query.get_or_404(customer_id)

        return customer

    @jwt_required()
    def delete(self, customer_id):
        customer = CustomerModel.query.get_or_404(customer_id)
        db.session.delete(customer)
        db.session.commit()

        return {"Message": "Customer deleted."}

    @jwt_required()
    @blp.arguments(CustomerUpdateSchema)
    @blp.response(200, CustomerSchema)
    def put(self, customer_data, customer_id):
        customer = CustomerModel.query.get(customer_id)
        if customer:
            for key, value in customer_data.items():
                setattr(customer, key, value)
        else:
            customer = CustomerModel(id=customer_id, **customer_data)

        db.session.add(customer)
        db.session.commit()

        return customer

@blp.route("/customer")
class CustomerList(MethodView):
    @jwt_required()
    @blp.response(200, CustomerSchema(many=True))
    def get(self):
        return CustomerModel.query.all()

    @jwt_required()
    @blp.arguments(CustomerSchema)
    @blp.response(201, CustomerSchema)
    def post(self, customer_data):
        customer = CustomerModel(**customer_data)

        try:
            db.session.add(customer)
            db.session.commit()
        except SQLAlchemyError:
            abort(500, message="An error occurred while inserting a new customer.")

        return customer
