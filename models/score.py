from db import db

class ScoreModel(db.Model):
    __tablename__ = "scores"

    id = db.Column(db.Integer, primary_key=True)
    datetime = db.Column(db.DateTime, nullable=False)
    transaction_id = db.Column(db.String(50), db.ForeignKey("transactions.id"), nullable=False, unique=True)
    score = db.Column(db.Float, nullable=False)
    # Relationships
    transaction = db.relationship("TransactionModel", back_populates="scores")