from flask import Blueprint, render_template, redirect, url_for, flash, session
from werkzeug.security import generate_password_hash, check_password_hash
from db import get_db_connection
from blueprints.utils import get_user_by_field, login_required, already_logged_in
from blueprints.sky_forms import RegistrationForm, LoginForm

auth_bp = Blueprint('auth', __name__)

# LOGIN REGISTER LOGOUT FUNCTIONS
def insert_user(username: str, phone_num: int, email: str, passwd: str):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO users (username, phone_num, email, passwd, acc_type) VALUES (%s, %s, %s, %s, %s)", (username, phone_num, email, passwd, "user"))
    conn.commit()
    cursor.close()
    conn.close()

# LOGIN REGISTER LOGOUT FUNCTIONS

# LOGIN REGISTER LOGOUT ROUTES
@auth_bp.route('/user/register', methods=['GET', 'POST'])
@already_logged_in
def register():
    registration_form = RegistrationForm()
    if registration_form.validate_on_submit():
        username = registration_form.username.data
        phone_num = registration_form.phone_num.data
        email = registration_form.email.data.lower()
        passwd = generate_password_hash(registration_form.passwd.data)
        insert_user(username, phone_num, email, passwd)
        flash('Account created!', 'success')
        return redirect(url_for('auth.user_login'))
    return render_template('user/register.html', registration_form=registration_form)

@auth_bp.route('/admin/login', methods=['GET', 'POST'])
@already_logged_in
def admin_login():
    login_form = LoginForm()
    if login_form.validate_on_submit():
        identifier = login_form.username_or_email.data
        passwd = login_form.passwd.data
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
            
        flash('Invalid username/email or password.', 'warning')
    return render_template('admin/admin_login.html', login_form=login_form)

@auth_bp.route('/user/login', methods=['GET', 'POST'])
@already_logged_in
def user_login():
    login_form = LoginForm()
    if login_form.validate_on_submit():
        identifier = login_form.username_or_email.data
        passwd = login_form.passwd.data
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
            
        flash('Invalid username/email or password.', 'warning')
    return render_template('user/user_login.html', login_form=login_form)

@auth_bp.route('/logout')
@login_required(['user', 'admin'])
def logout():
    session.clear()
    flash('Successfully logged out!', 'success')
    return redirect(url_for('homepage.home'))

# LOGIN REGISTER LOGOUT ROUTES