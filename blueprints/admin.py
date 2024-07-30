import requests
from flask import Blueprint, render_template, redirect, url_for, flash, abort, session, request
from werkzeug.security import check_password_hash
from urllib.parse import urlparse, urljoin
from flask_login import login_user, logout_user, current_user
from blueprints.utils import *
from blueprints.profile import handle_edit_form, delete_account
from blueprints.sky_forms import LoginForm, EditUsernameForm, EditPhoneNumForm, EditEmailForm, ResetPasswordForm, DeleteAccountForm
from blueprints.models import User
from db import get_db_connection

admin_bp = Blueprint('admin', __name__)

def is_safe_url(target):
    ref_url = urlparse(request.host_url)
    test_url = urlparse(urljoin(request.host_url, target))
    return test_url.scheme in ('http', 'https') and ref_url.netloc == test_url.netloc

def verify_recaptcha(response):
    secret = 'YOUR_RECAPTCHA_SECRET_KEY'
    payload = {
        'secret': secret,
        'response': response
    }
    response = requests.post('https://www.google.com/recaptcha/api/siteverify', data=payload)
    result = response.json()
    return result.get('success')

@admin_bp.route('/login', methods=['GET', 'POST'])
@already_logged_in
def admin_login():
    login_form = LoginForm()
    if login_form.validate_on_submit():
        identifier = login_form.username_or_email.data
        passwd = login_form.passwd.data
        remember = login_form.remember_me.data

        # Verify reCAPTCHA
        recaptcha_response = request.form.get('g-recaptcha-response')
        if not verify_recaptcha(recaptcha_response):
            flash('reCAPTCHA verification failed. Please try again.', 'warning')
            return redirect(url_for('admin.admin_login'))

        user_data = None

        # Check if the identifier is an email
        if '@' in identifier and '.' in identifier:
            user_data = get_user_by_field('email', identifier)
        else:
            user_data = get_user_by_field('username', identifier)

        if user_data and check_password_hash(user_data['passwd'], passwd):
            if user_data['acc_type'] == 'admin':
                user = User(user_data['user_id'], user_data['username'], user_data['passwd'], user_data['acc_type'])
                login_user(user, remember=remember)
                next_page = request.args.get('next')
                if not is_safe_url(next_page):
                    return abort(400)
                return redirect(next_page or url_for('admin.admin_profile'))
        flash('Invalid username/email or password.', 'warning')
    return render_template('admin/admin_login.html', login_form=login_form)
