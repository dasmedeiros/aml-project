from flask.views import MethodView
from flask_smorest import Blueprint, abort
from flask_jwt_extended import jwt_required, get_jwt
from sqlalchemy.exc import SQLAlchemyError

from db import db
from models import AccountModel, CustomerModel
from schemas import AccountSchema, AccountUpdateSchema

blp = Blueprint("Accounts", __name__, description="Operations on customer accounts")

@blp.route("/customer/<int:customer_id>/accounts")
class AccountsForCustomer(MethodView):
    #Gets every account for a specific customer
    @jwt_required(refresh=True)
    @blp.response(200, AccountSchema(many=True))
    def get(self, customer_id):
        accounts = AccountModel.query.filter_by(customer_id=customer_id).all()

        # Check if the result list is empty
        if not accounts:
            abort(404, message="This user has no associated account.")  # Return a 404 error response

        return accounts
    
    #Creates an account
    @jwt_required(refresh=True)    
    @blp.arguments(AccountSchema)
    @blp.response(201, AccountSchema)
    def post(self, account_data, customer_id):
        jwt = get_jwt()
        if not jwt.get("is_admin"):
            abort(401, message="Admin privilege required.")
        
        account = AccountModel(customer_id=customer_id, **account_data)

        try:
            db.session.add(account)
            db.session.commit()
        except SQLAlchemyError as e:
            abort(500, message=str(e))
        
        return account

@blp.route("/account/<int:account_id>/customer")
class AccountLink(MethodView):
    #Links an account to a specific customer
    @jwt_required(refresh=True)
    @blp.arguments(AccountUpdateSchema)
    @blp.response(201, AccountSchema)
    def post(self, account_id):
        jwt = get_jwt()
        if not jwt.get("is_admin"):
            abort(401, message="Admin privilege required.")
        
        account = AccountModel.query.get_or_404(account_id)

        # Extract customer_id from the request context
        customer_id = int(request.args.get("id"))
        customer = CustomerModel.query.get_or_404(customer_id)

        customer.accounts.append(account)

        try: 
            db.session.add(customer)
            db.session.commit()
        except SQLAlchemyError:
            abort(500, message="An error ocurred while inserting the account.")

        return account
    
@blp.route("/account/<int:account_id>")
class AccountCustomer(MethodView):
    #Get a specific account
    @jwt_required(refresh=True)
    @blp.response(200, AccountSchema)
    def get(self, account_id):
        account = AccountModel.query.get_or_404(account_id)
        
        return account

    #Delete a specific account
    @jwt_required(fresh=True)
    @blp.response(202, description="Deletes an account if no customer is associated with it.", example={"Message": "Account deleted."})
    @blp.alt_response(404, description="Account not found.")
    @blp.alt_response(400, description="Returned if the account is assigned to a customer. In this case, the account is not deleted.")
    def delete(self, account_id):
        jwt = get_jwt()["jti"]
        if not jwt.get("is_admin"):
            abort(401, message="Admin privilege required.")
        
        account = AccountModel.query.get_or_404(account_id)
        
        if not account.items():
            db.session.delete(account)
            db.session.commit()
            return {"message": "Account deleted."}
        abort(400, message="Could not delete account. Make sure account is not assiocated with a customer, then try again.")

        return account
    
    #Update a specific account
    @jwt_required(refresh=True)
    @blp.arguments(AccountUpdateSchema)
    @blp.response(200, AccountSchema)
    def put(self, account_data, account_id):
        account = AccountModel.query.get(account_id)
        if account:
            for key, value in account_data.items():
                setattr(account, key, value)
        else:
            account = AccountModel(id=account_id, **account_data)

        try:
            db.session.add(account)
            db.session.commit()
        except SQLAlchemyError as e:
            abort(500, message=str(e))

        return account

#Retrieve every account in the database
@blp.route("/accounts")
class AccountsList(MethodView):
    @jwt_required(refresh=True)
    @blp.response(200, AccountSchema(many=True))
    def get(self):
        return AccountModel.query.all()