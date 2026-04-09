from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from app.models.user import User
from app import bcrypt, login_manager

# Definimos el Blueprint para la autenticación
auth_bp = Blueprint('auth', __name__)

# Le indicamos a Flask-Login cómo buscar al usuario en la base de datos
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@auth_bp.route('/', methods=['GET', 'POST'])
@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    # Eliminamos el bloqueo automático para permitir "Cambiar de Usuario" si se accede a /login directamente
    
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        user = User.query.filter_by(username=username).first()
        
        if user and bcrypt.check_password_hash(user.password_hash, password):
            login_user(user)
            
            next_page = request.args.get('next')
            if next_page:
                return redirect(next_page)
                
            # REDIRECCIÓN INTELIGENTE AL INICIAR SESIÓN
            if user.role == 'admin':
                return redirect(url_for('dashboard.index'))
            elif user.role == 'cashier':
                return redirect(url_for('cashier.pos'))
            elif user.role == 'chef':
                return redirect(url_for('orders.kitchen'))
            else:
                return redirect(url_for('tables.monitor'))
        else:
            flash('Usuario o contraseña incorrectos. Intente nuevamente.', 'danger')
            
    return render_template('login.html')

@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard.index'))
        
    if request.method == 'POST':
        full_name = request.form.get('full_name')
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        
        from app import db
        # Revisar duplicados
        if User.query.filter_by(username=username).first():
            flash('El nombre de usuario ya existe.', 'danger')
            return redirect(url_for('auth.register'))
            
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
        new_user = User(
            full_name=full_name,
            username=username,
            email=email,
            password_hash=hashed_password,
            role='admin'
        )
        try:
            db.session.add(new_user)
            db.session.commit()
            flash('Restaurante registrado con éxito. Inicia sesión.', 'success')
            return redirect(url_for('auth.login'))
        except Exception as e:
            db.session.rollback()
            flash('Error al registrar. Intenta nuevamente.', 'danger')
            
    return render_template('register.html')