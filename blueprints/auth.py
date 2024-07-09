from flask import Blueprint, render_template, redirect, url_for, flash, session
from werkzeug.security import generate_password_hash, check_password_hash
from db import get_db_connection
from blueprints.sky_forms import RegistrationForm, LoginForm
from blueprints.utils import get_user_by_field

auth_bp = Blueprint('auth', __name__)

# LOGIN REGISTER LOGOUT FUNCTIONS
def get_max_user_id():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT MAX(user_id) FROM users")
    max_user_id = cursor.fetchone()[0]
    cursor.close()
    conn.close()
    return max_user_id

def insert_user(username: str, phone_num: int, email: str, passwd: str):
    conn = get_db_connection()
    cursor = conn.cursor()

    # Fetch the current maximum user_id
    max_user_id = get_max_user_id()
    if max_user_id is None:
        max_user_id = 0

    # Insert the new user
    cursor.execute("INSERT INTO users (user_id, username, phone_num, email, passwd, acc_type) VALUES (%s, %s, %s, %s, %s, %s)", (max_user_id + 1, username, phone_num, email, passwd, "user"))
    
    # Update AUTO_INCREMENT value if necessary
    cursor.execute("ALTER TABLE users AUTO_INCREMENT = %s", (max_user_id + 2,))
    
    conn.commit()
    cursor.close()
    conn.close()

# LOGIN REGISTER LOGOUT FUNCTIONS

# LOGIN REGISTER LOGOUT ROUTES
@auth_bp.route('/admin-login')
def admin_login():
    return render_template('admin/admin_login.html')

@auth_bp.route('/cust-login', methods=['GET', 'POST'])
def cust_login():
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        passwd = form.passwd.data
        user = get_user_by_field('username', username)
        if user and check_password_hash(user['passwd'], passwd):
            session['user_id'] = user['user_id']
            session['username'] = user['username']
            return redirect(url_for('init.homepage'))
        flash('Invalid username or password', 'warning')
    return render_template('customer/cust_login.html', form=form)

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        username = form.username.data
        phone_num = form.phone_num.data
        email = form.email.data
        passwd = generate_password_hash(form.passwd.data)
        insert_user(username, phone_num, email, passwd)
        return redirect(url_for('auth.cust_login'))
    return render_template('customer/register.html', form=form)

@auth_bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('auth.cust_login'))

# LOGIN REGISTER LOGOUT ROUTES