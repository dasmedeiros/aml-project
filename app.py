import os
import secrets

from flask import Flask, jsonify
from flask_smorest import Api
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate
from dotenv import load_dotenv

from db import db
import models
from models import BlocklistModel

from resources.account import blp as AccountsBlueprint
from resources.customer import blp as CustomersBlueprint
from resources.merchant import blp as MerchantsBlueprint
from resources.transaction import blp as TransactionsBlueprint
from resources.score import blp as ScoresBlueprint
from resources.user import blp as UsersBlueprint

def create_app(db_url=None):
    app = Flask(__name__)
    load_dotenv()

    app.config["PROPAGATE_EXCEPTIONS"] = True
    app.config["API_TITLE"] = "AML RESTful API"
    app.config["API_VERSION"] = "v1"
    app.config["OPENAPI_VERSION"] = "3.0.3"
    app.config["OPENAPI_URL_PREFIX"] = "/"
    app.config["OPENAPI_SWAGGER_UI_PATH"] = "/swagger-ui"
    app.config["OPENAPI_SWAGGER_UI_URL"] = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"
    app.config["SQLALCHEMY_DATABASE_URI"] = db_url or os.getenv("DATABASE_URL", "sqlite:///data.db")
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.init_app(app)
    migrate = Migrate(app, db)
    api = Api(app)

    app.config["JWT_SECRET_KEY"] = os.getenv("SECRET_KEY")
    jwt = JWTManager(app)

    @jwt.token_in_blocklist_loader
    def check_if_token_in_blocklist(jwt_header, jwt_payload):
        jti = jwt_payload["jti"]
        blocked_token = db.session.query(BlocklistModel).filter_by(jti=jti).first()
        return blocked_token is not None

    @jwt.revoked_token_loader
    def revoked_token_callback(jwt_header, jwt_payload):
        return(jsonify({"message": "The token has been revoked.", "error": "token_revoked"}), 401)
        
    @jwt.needs_fresh_token_loader
    def token_not_fresh_callback(jwt_header, jwt_payload):
        return(jsonify({"message": "The token is not fresh.", "error": "fresh_token_required"}), 401)

    @jwt.additional_claims_loader
    def add_claims_to_jwt(identity):
        # Look in the database if user is an admin
        if identity == 1:
            return {"is_admin": True}
        return {"is_admin": False}

    @jwt.expired_token_loader
    def expired_token_callback(jwt_header, jwt_payload):
        return(jsonify({"message": "The token has expired.", "error": "token_expired"}), 401)

    @jwt.invalid_token_loader
    def invalid_token_callback(error):
        return(jsonify({"message": "Signature verification failed.", "error": "invalid_token"}), 401)

    @jwt.unauthorized_loader
    def missing_token_callback(error):
        return(jsonify({"message": "Request does not contain an access token.", "error": "authorization_required"}), 401)

    api.register_blueprint(AccountsBlueprint)
    api.register_blueprint(CustomersBlueprint)
    api.register_blueprint(MerchantsBlueprint)
    api.register_blueprint(TransactionsBlueprint)
    api.register_blueprint(ScoresBlueprint)
    api.register_blueprint(UsersBlueprint)

    return app