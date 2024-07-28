from flask import Blueprint, render_template, redirect, url_for, flash, abort, request
from flask_login import login_user, login_required, logout_user
from werkzeug.security import generate_password_hash, check_password_hash
from urllib.parse import urlparse, urljoin
from db import get_db_connection
from blueprints.utils import *
from blueprints.sky_forms import RegistrationForm, LoginForm
from blueprints.models import User

auth_bp = Blueprint('auth', __name__)

# LOGIN REGISTER LOGOUT FUNCTIONS
def is_safe_url(target):
    ref_url = urlparse(request.host_url)
    test_url = urlparse(urljoin(request.host_url, target))
    return test_url.scheme in ('http', 'https') and ref_url.netloc == test_url.netloc

def insert_user(username: str, phone_num: int, email: str, passwd: str):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO users (username, phone_num, email, passwd, acc_type) VALUES (%s, %s, %s, %s, %s)", (username, phone_num, email, passwd, "user"))
    conn.commit()
    cursor.close()
    conn.close()

# LOGIN REGISTER LOGOUT FUNCTIONS

# LOGIN REGISTER LOGOUT ROUTES
@auth_bp.route('/register', methods=['GET', 'POST'])
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

@auth_bp.route('/login', methods=['GET', 'POST'])
@already_logged_in
def user_login():
    login_form = LoginForm()
    if login_form.validate_on_submit():
        identifier = login_form.username_or_email.data
        passwd = login_form.passwd.data
        user_data = None

        # Check if the identifier is an email
        if '@' in identifier and '.' in identifier:
            user_data = get_user_by_field('email', identifier)
        else:
            user_data = get_user_by_field('username', identifier)

        if user_data and check_password_hash(user_data['passwd'], passwd):
            if user_data['acc_type'] == 'user':
                user = User(user_data['user_id'], user_data['username'], user_data['passwd'], user_data['acc_type'])
                login_user(user)
                next_page = request.args.get('next')
                if not is_safe_url(next_page):
                    return abort(400)
                return redirect(next_page or url_for('homepage.home'))
        flash('Invalid username/email or password.', 'warning')
    return render_template('user/user_login.html', login_form=login_form)

@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Successfully logged out!', 'success')
    return redirect(url_for('homepage.home'))

# LOGIN REGISTER LOGOUT ROUTES