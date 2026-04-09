import sys
from app import create_app, db
from app.models.table import Table
from app.models.product import Product

app = create_app()
with app.app_context():
    try:
        new_table = Table(number="10", capacity="", location="Patio", qr_code="abc")
        db.session.add(new_table)
        db.session.commit()
        print("Table inserted with capacity=''")
    except Exception as e:
        print("Table insert error:", e)
        db.session.rollback()

    try:
        new_product = Product(name="Test", price="", category_id=None)
        db.session.add(new_product)
        db.session.commit()
        print("Product inserted with price=''")
    except Exception as e:
        print("Product insert error:", e)
        db.session.rollback()
