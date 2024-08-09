import secrets
from flask import Blueprint, render_template, redirect, url_for, flash, abort, request, current_app, session
from flask_login import login_user, login_required, logout_user
from werkzeug.security import generate_password_hash, check_password_hash
from urllib.parse import urlparse, urljoin
from db import get_db_connection
from blueprints.utils import *
from blueprints.sky_forms import RegistrationForm, LoginForm
from blueprints.models import User

auth_bp = Blueprint('auth', __name__)

def get_oauth():
    return current_app.extensions['authlib']['oauth']

def is_safe_url(target):
    ref_url = urlparse(request.host_url)
    test_url = urlparse(urljoin(request.host_url, target))
    return test_url.scheme in ('http', 'https') and ref_url.netloc == test_url.netloc

def insert_user(username: str, phone_num: int, email: str, passwd: str):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO users (username, phone_num, email, passwd, acc_type) VALUES (%s, %s, %s, %s, %s)",
                   (username, phone_num, email, passwd, "user"))
    conn.commit()
    cursor.close()
    conn.close()

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
        remember = login_form.remember_me.data
        user_data = None

        # Check if the identifier is an email
        if '@' in identifier and '.' in identifier:
            user_data = get_user_by_field('email', identifier)
        else:
            user_data = get_user_by_field('username', identifier)

        if user_data and check_password_hash(user_data['passwd'], passwd):
            if user_data['acc_type'] == 'user':
                user = User(user_data['user_id'], user_data['username'], user_data['passwd'], user_data['acc_type'])
                login_user(user, remember=remember)
                next_page = request.args.get('next')
                if not is_safe_url(next_page):
                    return abort(400)
                return redirect(next_page or url_for('homepage.home'))
        flash('Invalid username/email or password.', 'warning')
    return render_template('user/user_login.html', login_form=login_form)

@auth_bp.route('/login/google')
def google_login():
    google = get_oauth().create_client('google')
    state = secrets.token_urlsafe(16)
    nonce = secrets.token_urlsafe(16)
    session['oauth_state'] = state
    session['oauth_nonce'] = nonce
    print(f'Session before redirect: {session}')
    return google.authorize_redirect(url_for('auth.google_authorized', _external=True), state=state, nonce=nonce)
@auth_bp.route('/login/google/authorized')
def google_authorized():
    google = get_oauth().create_client('google')
    request_state = request.args.get('state')
    saved_state = session.pop('oauth_state', None)
    nonce = session.pop('nonce', None)

    # debug
    print(f'Session data at authorization callback: {session}')
    print(f'Request state: {request_state}')
    print(f'Saved state: {saved_state}')
    print(f'Nonce: {nonce}')

    if saved_state != request_state:
        flash('CSRF token mismatch. Possible attack detected.', 'danger')
        return redirect(url_for('auth.user_login'))

    token_response = google.authorize_access_token()
    if not token_response:
        flash('Authorization failed. Please try again.', 'danger')
        return redirect(url_for('auth.user_login'))

    user_info = google.parse_id_token(token_response, nonce=nonce)
    # debug
    print(f'User info: {user_info}')

    if not user_info:
        flash('Failed to fetch user information.', 'danger')
        return redirect(url_for('auth.user_login'))

    email = user_info.get('email')
    username = user_info.get('name', email)  # If 'name' is not present, use email as fallback

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute('SELECT * FROM users WHERE email = %s', (email,))
    user = cursor.fetchone()

    if not user:
        hashed_password = generate_password_hash('default_password')
        cursor.execute("INSERT INTO users (username, email, passwd, acc_type) VALUES (%s, %s, %s, %s)",
                       (username, email, hashed_password, 'user'))
        conn.commit()
        cursor.execute('SELECT * FROM users WHERE email = %s', (email,))
        user = cursor.fetchone()

    cursor.close()
    conn.close()

    user_obj = User(user['user_id'], user['username'], user['passwd'], user['acc_type'])
    login_user(user_obj)
    flash('You were successfully logged in with Google.', 'success')
    return redirect(url_for('homepage.home'))


@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Successfully logged out!', 'success')
    return redirect(url_for('homepage.home'))


