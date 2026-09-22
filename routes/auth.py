from functools import wraps
from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from models import Admin

auth_bp = Blueprint('auth', __name__)

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'admin_logged_in' not in session:
            flash('Please log in to access the administrator panel.', 'warning')
            return redirect(url_for('auth.admin_login'))
        return f(*args, **kwargs)
    return decorated_function

@auth_bp.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    if 'admin_logged_in' in session:
        return redirect(url_for('admin.dashboard'))
        
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '').strip()
        
        admin = Admin.query.filter_by(username=username).first()
        if admin and admin.check_password(password):
            session['admin_logged_in'] = True
            session['admin_username'] = admin.username
            flash('Successfully logged in to CoderesQ Admin Console.', 'success')
            return redirect(url_for('admin.dashboard'))
        else:
            flash('Invalid administrator credentials. Please try again.', 'error')
            
    return render_template('admin/login.html')

@auth_bp.route('/admin/logout')
def admin_logout():
    session.pop('admin_logged_in', None)
    session.pop('admin_username', None)
    flash('You have been logged out of the admin console.', 'info')
    return redirect(url_for('auth.admin_login'))
