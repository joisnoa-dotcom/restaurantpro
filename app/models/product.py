from app import db
from datetime import datetime, timezone

_now_utc = lambda: datetime.now(timezone.utc)

class Product(db.Model):
    __tablename__ = 'products'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    description = db.Column(db.Text)
    price = db.Column(db.Numeric(10, 2), default=0.0)
    cost = db.Column(db.Numeric(10, 2), default=0.0)
    image_url = db.Column(db.String(255))
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id', ondelete='CASCADE'))
    is_available = db.Column(db.Boolean, default=True)
    track_stock = db.Column(db.Boolean, default=False)
    stock = db.Column(db.Integer, default=0)
    preparation_time = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime(timezone=True), default=_now_utc)
    updated_at = db.Column(db.DateTime(timezone=True), default=_now_utc, onupdate=_now_utc)
    
    order_items = db.relationship('OrderItem', backref='product', lazy=True)
