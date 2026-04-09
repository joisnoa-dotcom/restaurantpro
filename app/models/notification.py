from app import db
from datetime import datetime

class Notification(db.Model):
    __tablename__ = 'notifications'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    type = db.Column(db.String(50), default='system')
    message = db.Column(db.Text, nullable=False)
    is_read = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    @property
    def time(self):
        return self.created_at.strftime('%H:%M') if self.created_at else ''
        
    @classmethod
    def get_unread_count(cls, user_id):
        return cls.query.filter_by(user_id=user_id, is_read=False).count()
        
    @classmethod
    def get_by_user(cls, user_id, limit=20):
        return cls.query.filter_by(user_id=user_id).order_by(cls.created_at.desc()).limit(limit).all()
        
    @classmethod
    def create(cls, message, type='system', user_id=None):
        n = cls(message=message, type=type, user_id=user_id)
        db.session.add(n)
        db.session.commit()
        return n
        
    def mark_as_read(self):
        self.is_read = True
        db.session.commit()
