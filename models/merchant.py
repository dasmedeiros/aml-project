from db import db

class MerchantModel(db.Model):
    __tablename__ = "merchants"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=False, nullable=False)
    industry = db.Column(db.String(80), unique=False, nullable=False)
    city = db.Column(db.String(80), unique=False, nullable=False)
    state = db.Column(db.String(80), unique=False, nullable=False)
    long = db.Column(db.Float(precision=2), unique=False, nullable=False)
    lat = db.Column(db.Float(precision=2), unique=False, nullable=False)
    # Relationships
    transactions = db.relationship("TransactionModel", back_populates="merchants")