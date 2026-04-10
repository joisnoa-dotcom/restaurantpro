from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from app.utils.decorators import role_required
from app.models.order import Order
from app.models.table import Table
from app.models.payment import Payment, Invoice
from app.models.notification import Notification 
from app.models.cash_register import CashSession
from app.models.audit_log import AuditLog
from datetime import datetime
from app import db
from app.utils.formatters import safe_float
import random

cashier_bp = Blueprint('cashier', __name__, url_prefix='/cashier')

@cashier_bp.route('/')
@login_required
@role_required('admin', 'cashier')
def pos():
    active_orders = Order.query.filter(Order.status.notin_(['paid', 'cancelled'])).order_by(Order.created_at.desc()).all()
    current_session = CashSession.query.filter_by(status='open').first()
    return render_template('cashier/pos.html', orders=active_orders, current_session=current_session)

@cashier_bp.route('/open_session', methods=['POST'])
@login_required
@role_required('admin')
def open_session():
    existing = CashSession.query.filter_by(status='open').first()
    if existing:
        flash('Ya existe una caja abierta.', 'warning')
        return redirect(url_for('cashier.pos'))
        
    opening_amount = safe_float(request.form.get('opening_amount'), default=0.0)
    
    new_session = CashSession(
        user_id=current_user.id,
        opening_amount=opening_amount,
        status='open'
    )
    db.session.add(new_session)
    db.session.flush()
    
    from app.models.audit_log import AuditLog
    AuditLog.log('OPEN_SESSION', 'cash_sessions', new_session.id, f"Caja abierta con monto inicial de S/ {opening_amount}", current_user.id)
    db.session.commit()
    
    flash('Caja abierta exitosamente.', 'success')
    return redirect(url_for('cashier.pos'))

@cashier_bp.route('/close_session', methods=['POST'])
@login_required
@role_required('admin')
def close_session():
    current_session = CashSession.query.filter_by(status='open').first()
    if not current_session:
        flash('No hay ninguna caja abierta para cerrar.', 'warning')
        return redirect(url_for('cashier.pos'))
        
    payments = Payment.query.filter_by(cash_session_id=current_session.id, status='completed').all()
    from app.models.cash_expense import CashExpense
    expenses = CashExpense.query.filter_by(cash_session_id=current_session.id).all()
    
    total_sales = sum(float(p.amount) for p in payments)
    cash_sales = sum(float(p.amount) for p in payments if p.payment_method == 'cash')
    total_expenses = sum(float(e.amount) for e in expenses)
    expected_amount = float(current_session.opening_amount) + cash_sales - total_expenses
    
    closing_amount = safe_float(request.form.get('closing_amount'), default=expected_amount)
    
    current_session.closing_time = datetime.utcnow()
    current_session.closing_amount = closing_amount
    current_session.expected_amount = expected_amount
    current_session.status = 'closed'
    
    from app.models.audit_log import AuditLog
    AuditLog.log('CLOSE_SESSION', 'cash_sessions', current_session.id, f"Caja cerrada. Monto Esperado: S/ {expected_amount}, Ingresado: S/ {closing_amount}", current_user.id)
    db.session.commit()
    
    flash(f'Caja cerrada. Ventas puras: S/ {total_sales} | Egresos: S/ {total_expenses}. Revisa tu Ticket Z a continuación.', 'success')
    return redirect(url_for('reports.shift_ticket', session_id=current_session.id))

@cashier_bp.route('/add_expense', methods=['POST'])
@login_required
@role_required('admin', 'cashier')
def add_expense():
    current_session = CashSession.query.filter_by(status='open').first()
    if not current_session:
        flash('No hay ninguna caja abierta para registrar egresos.', 'danger')
        return redirect(url_for('cashier.pos'))
        
    amount = safe_float(request.form.get('amount'), default=0.0)
    reason = request.form.get('reason')
    
    try:
        from app.models.cash_expense import CashExpense
        expense = CashExpense(
            cash_session_id=current_session.id,
            user_id=current_user.id,
            amount=float(amount),
            reason=reason
        )
        db.session.add(expense)
        
        from app.models.audit_log import AuditLog
        AuditLog.log('CASH_EXPENSE', 'cash_expenses', current_session.id, f"Egreso de caja: S/ {amount} por {reason}", current_user.id)
        
        db.session.commit()
        flash(f'Se registró con éxito el egreso por S/ {amount}.', 'success')
    except Exception as e:
        db.session.rollback()
        flash('Hubo un error al registrar el egreso.', 'danger')
        
    return redirect(url_for('cashier.pos'))

@cashier_bp.route('/checkout/<int:order_id>')
@login_required
@role_required('admin', 'cashier')
def checkout(order_id):
    current_session = CashSession.query.filter_by(status='open').first()
    if not current_session:
        flash('Es necesario que un Administrador abra la caja antes de cobrar.', 'danger')
        return redirect(url_for('cashier.pos'))

    order = Order.query.get_or_404(order_id)
    if order.status == 'paid':
        flash('Este pedido ya fue pagado.', 'warning')
        return redirect(url_for('cashier.pos'))
        
    return render_template('cashier/payments.html', order=order)

@cashier_bp.route('/pay/<int:order_id>', methods=['POST'])
@login_required
@role_required('admin', 'cashier')
def pay(order_id):
    current_session = CashSession.query.filter_by(status='open').first()
    if not current_session:
        flash('No hay caja abierta. Es necesario que un Administrador abra la caja antes de poder cobrar.', 'danger')
        return redirect(url_for('cashier.pos'))

    order = Order.query.get_or_404(order_id)
    
    # Bloqueo de concurrencia: Evitar cobros dobles si alguien clica múltiples veces
    if order.status == 'paid':
        flash('Seguridad: Esta orden ya fue cobrada previamente.', 'warning')
        return redirect(url_for('cashier.pos'))
    
    amount = safe_float(request.form.get('amount'), default=0.0)
    payment_method = request.form.get('payment_method')
    reference_code = request.form.get('reference_code', '')
    invoice_type = request.form.get('invoice_type')
    customer_name = request.form.get('customer_name', 'Cliente Varios')
    customer_document = request.form.get('customer_document', '00000000')
    
    try:
        payment = Payment(
            order_id=order.id, amount=amount, payment_method=payment_method,
            reference_code=reference_code, status='completed', created_by=current_user.id,
            cash_session_id=current_session.id
        )
        db.session.add(payment)
        db.session.flush() 
        
        prefix = 'B001' if invoice_type == 'boleta' else 'F001'
        last_invoice = Invoice.query.filter(Invoice.document_number.like(f"{prefix}-%")).order_by(Invoice.id.desc()).first()
        next_num = 1
        if last_invoice:
            try:
                next_num = int(last_invoice.document_number.split('-')[1]) + 1
            except (ValueError, IndexError):
                next_num = random.randint(100000, 999999)
        doc_number = f"{prefix}-{next_num:06d}"
        
        total = float(amount)
        subtotal = total / 1.18
        tax_amount = total - subtotal
        
        invoice = Invoice(
            payment_id=payment.id, invoice_type=invoice_type, document_number=doc_number,
            customer_name=customer_name, customer_document=customer_document,
            subtotal=subtotal, tax_amount=tax_amount, total_amount=total
        )
        db.session.add(invoice)
        
        order.status = 'paid'
        table = Table.query.get(order.table_id)
        
        if table:
            unreads = Notification.query.filter(
                Notification.is_read == False,
                Notification.message.like(f"%Mesa {table.number}%")
            ).all()
            for n in unreads:
                n.is_read = True
            
            table.status = 'free'
            
        db.session.commit()
        # (Supabase Realtime)
        if table:
            msg = f'¡Cobro exitoso! Se generó la {invoice_type.capitalize()} {doc_number}. La Mesa {table.number} ahora está libre.'
        else:
            tipo = 'Delivery' if order.order_type == 'delivery' else 'Para Llevar'
            msg = f'¡Cobro exitoso! Se generó la {invoice_type.capitalize()} {doc_number} para la orden tipo {tipo}.'
        flash(msg, 'success')
        # UX FIx: Redirigimos directamente al Ticket para imprimir, en lugar de perder el control de la cuenta
        return redirect(url_for('cashier.ticket', order_id=order.id))
        
        
    except Exception as e:
        db.session.rollback()
        flash('Ocurrió un error al procesar el pago.', 'danger')
        print(e)
        
    return redirect(url_for('cashier.pos'))

@cashier_bp.route('/ticket/<int:order_id>')
@login_required
def ticket(order_id):
    order = Order.query.get_or_404(order_id)
    payment = Payment.query.filter_by(order_id=order.id).first()
    invoice = Invoice.query.filter_by(payment_id=payment.id).first() if payment else None
    return render_template('cashier/ticket.html', order=order, payment=payment, invoice=invoice)