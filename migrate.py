import sys
import os

# Añadir el raíz para que importe app sin problemas
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app import create_app, db
from sqlalchemy import text

app = create_app()

with app.app_context():
    try:
        # Hacer table_id nullable y no foránea restrictiva si falla, pero el schema de mysql lo permite nullable
        db.session.execute(text('ALTER TABLE orders MODIFY table_id int(11) DEFAULT NULL'))
        
        # Añadir las nuevas columnas
        db.session.execute(text("ALTER TABLE orders ADD COLUMN order_type enum('dine_in','takeaway','delivery') DEFAULT 'dine_in'"))
        db.session.execute(text("ALTER TABLE orders ADD COLUMN customer_name varchar(100) DEFAULT NULL"))
        db.session.execute(text("ALTER TABLE orders ADD COLUMN customer_phone varchar(20) DEFAULT NULL"))
        db.session.execute(text("ALTER TABLE orders ADD COLUMN delivery_address text DEFAULT NULL"))
        db.session.execute(text("ALTER TABLE orders ADD COLUMN delivery_fee decimal(10,2) DEFAULT 0.00"))
        
        db.session.commit()
        print("Migración completada exitosamente.")
    except Exception as e:
        print(f"Error durante migración: {e}")
