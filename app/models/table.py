from app import db
from datetime import datetime

class Table(db.Model):
    __tablename__ = 'tables'
    id = db.Column(db.Integer, primary_key=True)
    number = db.Column(db.Integer, unique=True, nullable=False)
    capacity = db.Column(db.Integer, nullable=False, default=4)
    status = db.Column(db.String(50), default='free')
    location = db.Column(db.String(100))
    qr_code = db.Column(db.String(255))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    orders = db.relationship('Order', backref='table_rel', lazy=True)
