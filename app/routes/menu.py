from flask import Blueprint, render_template, request, jsonify
from app.models.table import Table
from app.models.product import Product
from app.models.category import Category
from app.models.order import Order, OrderItem
from app.models.notification import Notification
from app import db
import random
import string

menu_bp = Blueprint('menu', __name__, url_prefix='/menu')

# 1. RUTA PARA MOSTRAR LA CARTA (No requiere login)
@menu_bp.route('/<qr_code>')
def view_menu(qr_code):
    # Buscamos la mesa por su código secreto
    table = Table.query.filter_by(qr_code=qr_code).first_or_404()
    categories = Category.query.filter_by(is_active=True).all()
    products = Product.query.filter_by(is_available=True).all()
    
    return render_template('carta-digital.html', table=table, categories=categories, products=products)

# 2. RUTA PARA RECIBIR EL PEDIDO DESDE EL CELULAR DEL CLIENTE
@menu_bp.route('/<qr_code>/order', methods=['POST'])
def place_order(qr_code):
    table = Table.query.filter_by(qr_code=qr_code).first_or_404()
    data = request.json
    cart = data.get('cart', [])

    if not cart:
        return jsonify({'error': 'El carrito está vacío'}), 400

    # Verificamos si la mesa ya tiene una cuenta abierta para sumarle los platos, o si creamos una nueva
    active_order = Order.query.filter_by(table_id=table.id).filter(Order.status.in_(['pending', 'preparing', 'ready', 'served'])).first()

    if not active_order:
        chars = string.ascii_uppercase + string.digits
        order_num = 'WEB-' + ''.join(random.choices(chars, k=5))
        active_order = Order(
            table_id=table.id,
            user_id=None, # Pedido Web (Sin mozo)
            order_number=order_num,
            status='pending',
            total_amount=0
        )
        table.status = 'occupied'
        db.session.add(active_order)
        db.session.flush()

    total_added = 0
    for item in cart:
        product = Product.query.get(item['id'])
        if product:
            qty = item['cantidad']
            subtotal = float(product.price) * qty
            total_added += subtotal
            new_item = OrderItem(
                order_id=active_order.id,
                product_id=product.id,
                quantity=qty,
                unit_price=product.price,
                subtotal=subtotal,
                status='pending',
                notes=item.get('notas', '')
            )
            db.session.add(new_item)

    active_order.total_amount = float(active_order.total_amount) + total_added

    # Notificamos al sistema interno
    Notification.create(
        type='system', 
        message=f"¡Nuevo pedido WEB recibido en la Mesa {table.number}!", 
        user_id=None
    )

    db.session.commit()
    
    # (Supabase Realtime)

    return jsonify({'success': True, 'message': 'Pedido enviado a cocina'})