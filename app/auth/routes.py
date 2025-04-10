from flask import render_template, redirect, url_for, request, flash, session
from app import db
from app.models import User
from app.auth import bp

@bp.route('/register', methods=['GET', 'POST'])
def register():
    """
    Register a new user account.
    """
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        unit_preference = request.form.get('unit_preference', 'metric')
        height = request.form.get('height')

        if not username or not password:
            flash("Username and password are required.")
            return redirect(url_for('auth.register'))

        if User.query.filter_by(username=username).first():
            flash("Username already exists.")
            return redirect(url_for('auth.register'))

        try:
            height = float(height) if height else None
        except ValueError:
            height = None

        user = User(username=username, password=password, unit_preference=unit_preference, height=height)
        db.session.add(user)
        db.session.commit()
        flash("Registration successful. Please login.")
        return redirect(url_for('auth.login'))
    return render_template('auth/register.html')

@bp.route('/login', methods=['GET', 'POST'])
def login():
    """
    Log in a user.
    """
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = User.query.filter_by(username=username, password=password).first()
        if user:
            session['user_id'] = user.id
            return redirect(url_for('main.dashboard'))
        flash("Invalid username or password.")
    return render_template('auth/login.html')

@bp.route('/logout')
def logout():
    """
    Log out the current user.
    """
    session.pop('user_id', None)
    flash("Logged out successfully.")
    return redirect(url_for('auth.login'))
