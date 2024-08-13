import secrets
from flask import Blueprint, render_template, redirect, url_for, flash, abort, request, current_app, session
from flask_login import login_user, login_required, logout_user
from werkzeug.security import generate_password_hash, check_password_hash
from urllib.parse import urlparse, urljoin
from db import get_db_connection
from blueprints.utils import *
from blueprints.sky_forms import RegistrationForm, LoginForm, OTPForm, ForgotPasswordForm
from blueprints.models import User
import pyotp

auth_bp = Blueprint('auth', __name__)

def forgot_passwd(user_id):
    passwd = secrets.token_hex(16)
    hashed_passwd = generate_password_hash(passwd)
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE users SET passwd = %s WHERE user_id = %s", (hashed_passwd, user_id))
    conn.commit()
    cursor.close()
    conn.close()
    return passwd

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
            if user_data['acc_type'] == 'banned':
                flash('Your account is banned and cannot be accessed. Please submit an unban request form.', 'danger')
                return redirect(url_for('auth.user_login'))
            if user_data['acc_type'] == 'user':
                otp_secret = pyotp.random_base32()
                totp = pyotp.TOTP(otp_secret, interval=60)
                otp_code = totp.now()
                send_otp(user_data['email'], otp_code)
                session['otp_user_id'] = user_data['user_id']
                session['otp_remember'] = remember
                session['otp_secret'] = otp_secret
                return redirect(url_for('auth.otp_verification'))

        flash('Invalid username/email or password.', 'warning')
    return render_template('user/user_login.html', login_form=login_form)

@auth_bp.route('/otp_verification', methods=['GET', 'POST'])
@already_logged_in
def otp_verification():
    otp_form = OTPForm()
    if otp_form.validate_on_submit():
        user_id = session.get('otp_user_id')
        remember = session.get('otp_remember', False)
        otp_code = otp_form.otp.data
        otp_secret = session.get('otp_secret')

        if not otp_secret:
            flash('OTP verification failed. Please try again.', 'warning')
            return redirect(url_for('auth.user_login'))

        totp = pyotp.TOTP(otp_secret, interval=60)
        user_data = get_user_by_field('user_id', user_id)
        if user_data and totp.verify(otp_code, valid_window=1):
            user = User(user_data['user_id'], user_data['username'], user_data['passwd'], user_data['acc_type'])
            login_user(user, remember=remember)
            session.pop('otp_user_id', None)
            session.pop('otp_remember', None)
            session.pop('otp_secret', None)
            next_page = request.args.get('next')
            if not is_safe_url(next_page):
                return abort(400)
            return redirect(next_page or url_for('homepage.home'))
        else:
            flash('OTP is incorrect or has expired, please try again.', 'warning')
            return redirect(url_for('auth.user_login'))

    return render_template('misc/otp_verify.html', otp_form=otp_form)

@auth_bp.route('/forgot_password', methods=['GET', 'POST'])
def forgot_password():
    forgot_password_form = ForgotPasswordForm()
    if forgot_password_form.validate_on_submit():
        username = forgot_password_form.username.data
        email = forgot_password_form.email.data
        user = get_user_by_field('username', username)
        if user and user['email'] == email:
            passwd = forgot_passwd(user['user_id'])
            send_forgot_passwd(email, passwd)
            flash('Email sent', 'success')
            return redirect(url_for('auth.user_login'))
        else:
            flash('Invalid username or email', 'danger')
    return render_template('misc/forgot_passwd.html', forgot_password_form=forgot_password_form)

@auth_bp.route('/login/google')
def google_login():
    google = get_oauth().create_client('google')

    # generate a secure state and nonce for CSRF protection
    state = secrets.token_urlsafe(16)
    nonce = secrets.token_urlsafe(16)

    # for later validation
    session['oauth_state'] = state
    session['oauth_nonce'] = nonce
    print(f'Session before redirect: {session}')

    # redirect to google's authorization page
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
    username = user_info.get('name', email)

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


