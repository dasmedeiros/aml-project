from db import db

class AccountModel(db.Model):
    __tablename__ = "accounts"

    id = db.Column(db.String(50), primary_key=True)
    currency = db.Column(db.String(3), unique=False, nullable=False)
    balance = db.Column(db.Float(precision=2), unique=False, nullable=False)
    movement = db.Column(db.String(1), unique=False, nullable=False)
    customer_id = db.Column(db.String(50), db.ForeignKey("customers.id"), nullable=False)
    # Relationships
    customers = db.relationship("CustomerModel", back_populates="accounts")
    transactions = db.relationship("TransactionModel", back_populates="accounts")