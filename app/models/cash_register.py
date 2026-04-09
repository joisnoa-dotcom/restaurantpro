from app import db
from datetime import datetime

class CashSession(db.Model):
    __tablename__ = 'cash_sessions'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    opening_time = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    closing_time = db.Column(db.DateTime, nullable=True)
    opening_amount = db.Column(db.Numeric(10, 2), nullable=False)
    closing_amount = db.Column(db.Numeric(10, 2), nullable=True)
    expected_amount = db.Column(db.Numeric(10, 2), nullable=True)
    status = db.Column(db.String(50), default='open')
    
    user = db.relationship('User', backref='cash_sessions', lazy=True)
