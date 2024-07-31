from flask import Blueprint, render_template, redirect, url_for, flash, abort, session, request
from werkzeug.security import check_password_hash
from urllib.parse import urlparse, urljoin
from flask_login import login_user, logout_user, login_required
from blueprints.utils import *
from blueprints.profile import handle_edit_form, delete_account
from blueprints.sky_forms import LoginForm, EditUsernameForm, EditPhoneNumForm, EditEmailForm, ResetPasswordForm, DeleteAccountForm
from blueprints.models import User

admin_bp = Blueprint('admin', __name__)

def is_safe_url(target):
    ref_url = urlparse(request.host_url)
    test_url = urlparse(urljoin(request.host_url, target))
    return test_url.scheme in ('http', 'https') and ref_url.netloc == test_url.netloc

# ADMIN ROUTES
@admin_bp.route('/login', methods=['GET', 'POST'])
@already_logged_in
def admin_login():
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
            if user_data['acc_type'] == 'admin':
                user = User(user_data['user_id'], user_data['username'], user_data['passwd'], user_data['acc_type'])
                login_user(user, remember=remember)
                next_page = request.args.get('next')
                if not is_safe_url(next_page):
                    return abort(400)
                return redirect(next_page or url_for('admin.admin_profile'))
        flash('Invalid username/email or password.', 'warning')
    return render_template('admin/admin_login.html', login_form=login_form)

@admin_bp.route('/admin/profile', methods=['GET', 'POST'])
@admin_required
def admin_profile():
    user = get_user_by_field('user_id', session['_user_id'])
    edit_username_form = EditUsernameForm()
    edit_phone_num_form = EditPhoneNumForm()
    edit_email_form = EditEmailForm()
    reset_password_form = ResetPasswordForm()
    delete_account_form = DeleteAccountForm()
    if edit_username_form.new_username.name in request.form:
        message = 'Username changed!'
        if handle_edit_form(edit_username_form, user, 'username', 'new_username', message):
            return redirect(url_for('admin.admin_profile'))
    elif edit_phone_num_form.new_phone_num.name in request.form:
        message = 'Phone number changed!'
        if handle_edit_form(edit_phone_num_form, user, 'phone_num', 'new_phone_num', message):
            return redirect(url_for('admin.admin_profile'))
    elif edit_email_form.new_email.name in request.form:
        message = 'Email changed!'
        if handle_edit_form(edit_email_form, user, 'email', 'new_email', message, is_email=True):
            return redirect(url_for('admin.admin_profile'))
    elif reset_password_form.new_passwd.name in request.form:
        message = 'Password changed!'
        if handle_edit_form(reset_password_form, user, 'passwd', 'new_passwd', message, is_password=True):
            return redirect(url_for('admin.admin_profile'))
    return render_template('admin/admin_profile.html', user=user, edit_username_form=edit_username_form, edit_phone_num_form=edit_phone_num_form, edit_email_form=edit_email_form, reset_password_form=reset_password_form, delete_account_form=delete_account_form)

@admin_bp.route('/profile/delete', methods=['POST'])
@login_required
def delete_profile():
    delete_account_form = DeleteAccountForm()
    if delete_account_form.validate_on_submit():
        user_id = session['_user_id']
        delete_account(user_id)
        logout_user()
        flash('Account successfully deleted.', 'success')
        return redirect(url_for('homepage.home'))
    return render_template('admin/admin_profile.html', delete_account_form=delete_account_form)

@admin_bp.route('/user-management')
@admin_required
def user_management():
    users = get_all_users(session['_user_id'])
    return render_template('admin/user_management.html', users=users)

@admin_bp.route('/user-profile')
@admin_required
def user_profile():
    return render_template('admin/user_profile.html')
# ADMIN ROUTES