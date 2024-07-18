from flask import Blueprint, render_template, redirect, url_for, flash, session
from werkzeug.security import generate_password_hash, check_password_hash
from db import get_db_connection
from blueprints.sky_forms import RegistrationForm, LoginForm
from blueprints.utils import get_user_by_field, login_required, already_logged_in

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
@auth_bp.route('/admin/login', methods=['GET', 'POST'])
@already_logged_in
def admin_login():
    form = LoginForm()
    if form.validate_on_submit():
        identifier = form.username_or_email.data
        passwd = form.passwd.data
        user = None

        # Check if the identifier is an email
        if '@' in identifier and '.' in identifier:
            user = get_user_by_field('email', identifier)
        else:
            user = get_user_by_field('username', identifier)

        if user and check_password_hash(user['passwd'], passwd):
            session.clear()
            session['user_id'] = user['user_id']
            session['username'] = user['username']
            if user['acc_type'] == 'admin':
                return redirect(url_for('admin.admin_profile'))
            
        session.clear()
        flash('Invalid username/email or password.', 'warning')
    return render_template('admin/admin_login.html', form=form)

@auth_bp.route('/user/login', methods=['GET', 'POST'])
@already_logged_in
def user_login():
    form = LoginForm()
    if form.validate_on_submit():
        identifier = form.username_or_email.data
        passwd = form.passwd.data
        user = None

        # Check if the identifier is an email
        if '@' in identifier and '.' in identifier:
            user = get_user_by_field('email', identifier)
        else:
            user = get_user_by_field('username', identifier)

        if user and check_password_hash(user['passwd'], passwd):
            session.clear()
            session['user_id'] = user['user_id']
            session['username'] = user['username']
            if user['acc_type'] == 'user':
                return redirect(url_for('homepage.home'))
            
        session.clear()
        flash('Invalid username/email or password.', 'warning')
    return render_template('user/user_login.html', form=form)

@auth_bp.route('/user/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        username = form.username.data
        phone_num = form.phone_num.data
        email = form.email.data.lower()
        passwd = generate_password_hash(form.passwd.data)
        insert_user(username, phone_num, email, passwd)
        flash('Account created!', 'success')
        return redirect(url_for('auth.user_login'))
    return render_template('user/register.html', form=form)

@auth_bp.route('/logout')
@login_required(['user', 'admin'])
def logout():
    session.clear()
    flash('Successfully logged out!', 'success')
    return redirect(url_for('homepage.home'))

"""@auth_bp.route('/logout')
@login_required(['user', 'admin'])
def logout():
    user = get_user_by_field('user_id', session['user_id']) 
    session.clear()
    if user['acc_type'] == 'user':
        return redirect(url_for('auth.user_login'))
    elif user['acc_type'] == 'admin':
        return redirect(url_for('auth.admin_login'))"""

# LOGIN REGISTER LOGOUT ROUTES