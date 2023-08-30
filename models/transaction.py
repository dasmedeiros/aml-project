from db import db

class TransactionModel(db.Model):
    __tablename__ = 'transactions'

    # Transaction details
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime, nullable=False)
    status = db.Column(db.String(20), nullable=False)
    card_present_flag = db.Column(db.Integer, nullable=False)
    bpay_biller_code = db.Column(db.String(20), nullable=True)
    long = db.Column(db.Float(precision=2), unique=False, nullable=False)
    lat = db.Column(db.Float(precision=2), unique=False, nullable=False)
    txn_description = db.Column(db.String(50), nullable=False)
    amount = db.Column(db.Float(precision=2), nullable=False)
    currency = db.Column(db.String(3), nullable=False)
    movement = db.Column(db.String(10), nullable=False)
    # Merchant Details
    merchant_id = db.Column(db.Integer, db.ForeignKey("merchants.id"), unique=False, nullable=False)
    # Customer details
    customer_id = db.Column(db.Integer, db.ForeignKey("customers.id"), unique=False, nullable=False)
    # Account details
    account_id = db.Column(db.Integer, db.ForeignKey("accounts.id"), unique=False, nullable=False)
    # Relationships
    merchants = db.relationship("MerchantModel", back_populates="transactions")
    customers = db.relationship("CustomerModel", back_populates="transactions")
    accounts = db.relationship("AccountModel", back_populates="transactions")
    scores = db.relationship("ScoreModel", back_populates="transaction")