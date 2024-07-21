from flask import Blueprint, render_template, redirect, url_for, flash, session, request
from blueprints.utils import get_user_by_field, login_required
from blueprints.profile import handle_edit_form, delete_account
from blueprints.sky_forms import EditUsernameForm, EditPhoneNumForm, EditEmailForm, ResetPasswordForm, DeleteAccountForm

admin_bp = Blueprint('admin', __name__)

# ADMIN ROUTES
@admin_bp.route('/admin/profile', methods=['GET', 'POST'])
@login_required(['admin'])
def admin_profile():
    user = get_user_by_field('username', session['username'])

    edit_username_form = EditUsernameForm()
    edit_phone_num_form = EditPhoneNumForm()
    edit_email_form = EditEmailForm()
    reset_password_form = ResetPasswordForm()
    delete_account_form = DeleteAccountForm()

    if edit_username_form.new_username.name in request.form:
        message = 'Username changed!'
        if handle_edit_form(edit_username_form, user, 'username', 'new_username', message):
            return redirect(url_for('profile.my_profile'))
    elif edit_phone_num_form.new_phone_num.name in request.form:
        message = 'Phone number changed!'
        if handle_edit_form(edit_phone_num_form, user, 'phone_num', 'new_phone_num', message):
            return redirect(url_for('profile.my_profile'))
    elif edit_email_form.new_email.name in request.form:
        message = 'Email changed!'
        if handle_edit_form(edit_email_form, user, 'email', 'new_email', message, is_email=True):
            return redirect(url_for('profile.my_profile'))
    elif reset_password_form.new_passwd.name in request.form:
        message = 'Password changed!'
        if handle_edit_form(reset_password_form, user, 'passwd', 'new_passwd', message, is_password=True):
            return redirect(url_for('profile.my_profile'))

    return render_template('admin/admin_profile.html', user=user, edit_username_form=edit_username_form, edit_phone_num_form=edit_phone_num_form, edit_email_form=edit_email_form, reset_password_form=reset_password_form, delete_account_form=delete_account_form)

@admin_bp.route('/admin/profile/delete', methods=['POST'])
@login_required(['admin'])
def delete_profile():
    delete_account_form = DeleteAccountForm()
    if delete_account_form.validate_on_submit():
        user_id = session['user_id']
        delete_account(user_id)
        session.clear()
        flash('Account successfully deleted.', 'success')
        return redirect(url_for('homepage.home'))
    return render_template('admin/admin_profile.html', delete_account_form=delete_account_form)

@admin_bp.route('/admin/user-management')
@login_required(['admin'])
def user_management():
    return render_template('admin/user_management.html')

@admin_bp.route('/admin/user-profile')
@login_required(['admin'])
def user_profile():
    return render_template('admin/user_profile.html')

# ADMIN ROUTES
