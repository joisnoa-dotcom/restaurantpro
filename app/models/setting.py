from app import db

class Setting(db.Model):
    __tablename__ = 'settings'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), default='RestaurantPro')
    subtitle = db.Column(db.String(150), default='Sistema POS')
    ruc = db.Column(db.String(20), default='')
    address = db.Column(db.String(200), default='')
    phone = db.Column(db.String(50), default='')
    thank_you_message = db.Column(db.String(200), default='Gracias por su preferencia!')
    logo_url = db.Column(db.String(255), nullable=True)
