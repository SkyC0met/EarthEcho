from functools import wraps
from flask import session, redirect, url_for, flash
from db import get_db_connection
# import jwt

def login_required(roles):
    def wrapper(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if 'user_id' not in session:
                flash('Please log in to access this page.', 'danger')
                return redirect(url_for('auth.user_login'))

            user = get_user_by_field('user_id', session['user_id'])
            acc_type = user['acc_type']
            if acc_type is None:
                flash('Your session is invalid. Please log in.', 'danger')
                return redirect(url_for('auth.user_login'))
                
            if acc_type not in roles:
                flash("Unauthorised access.", 'danger')
                if acc_type == 'user':
                    return redirect(url_for('homepage.home'))
                elif acc_type == 'admin':
                    return redirect(url_for('admin.admin_profile'))
            return f(*args, **kwargs)
        return decorated_function
    return wrapper

def already_logged_in(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' in session:
            flash('You are already logged in.', 'primary')
            user = get_user_by_field('user_id', session['user_id'])
            acc_type = user['acc_type']
            if acc_type == 'admin':
                return redirect(url_for('admin.admin_profile'))
            elif acc_type == 'user':
                return redirect(url_for('homepage.home'))
        return f(*args, **kwargs)
    return decorated_function

def get_user_by_field(field_name: str, field_value):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    query = f"SELECT * FROM users WHERE {field_name} = %s"
    cursor.execute(query, (field_value,))
    user = cursor.fetchone()
    cursor.close()
    conn.close()
    return user

def get_all_users(exclude_user_id: int):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM users WHERE user_id != %s", (exclude_user_id,))
    users = cursor.fetchall()
    cursor.close()
    conn.close()
    return users