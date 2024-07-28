from flask import redirect, url_for, flash
from flask_login import LoginManager, current_user
from functools import wraps
from db import get_db_connection
from blueprints.models import User

login_manager = LoginManager()

@login_manager.user_loader
def load_user(user_id):
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT * FROM users WHERE user_id = %s", (user_id,))
    user = cursor.fetchone()
    cursor.close()
    connection.close()
    if user:
        return User(user['user_id'], user['username'], user['passwd'], user['acc_type'])
    return None

def role_required(role):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not current_user.is_authenticated:
                return login_manager.unauthorized()
            if current_user.acc_type != role:
                if role == 'admin':
                    flash('Unauthorized access.', 'danger')
                return redirect(url_for('homepage.home'))
            return f(*args, **kwargs)
        return decorated_function
    return decorator

admin_required = role_required('admin')
user_required = role_required('user')

def already_logged_in(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if current_user.is_authenticated:
            if current_user.is_authenticated:
                flash('Already logged in', "primary")
                return redirect(url_for('homepage.home'))  # Redirect to dashboard or any other page
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
