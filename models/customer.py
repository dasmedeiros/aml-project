from db import db

class CustomerModel(db.Model):
    __tablename__ = "customers"

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(80), unique=False, nullable=False)
    last_name = db.Column(db.String(80), unique=False, nullable=False)
    gender = db.Column(db.String(1), unique=False, nullable=False)
    age = db.Column(db.Integer, unique=False, nullable=False)
    city = db.Column(db.String(80), unique=False, nullable=False)
    state = db.Column(db.String(80), unique=False, nullable=False)
    # Relationships
    accounts = db.relationship("AccountModel", back_populates="customers")
    transactions = db.relationship("TransactionModel", back_populates="customers")