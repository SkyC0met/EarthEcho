from flask import Blueprint, render_template, redirect, url_for, flash, session, request
from blueprints.utils import get_user_by_field, login_required
from werkzeug.security import check_password_hash, generate_password_hash
from blueprints.sky_forms import EditUsernameForm, EditPhoneNumForm, EditEmailForm, ResetPasswordForm, DeleteAccountForm
from blueprints.profile import update_user_field, handle_edit_form, delete_account

admin_bp = Blueprint('admin', __name__)

#SKY ADMIN ROUTES
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
            return redirect(url_for('admin.admin_profile'))
    elif edit_phone_num_form.new_phone_num.name in request.form:
        message = 'Phone number changed!'
        if handle_edit_form(edit_phone_num_form, user, 'phone_num', 'new_phone_num', message):
            return redirect(url_for('admin.admin_profile'))
    elif edit_email_form.new_email.name in request.form:
        if edit_email_form.validate_on_submit():
            new_email = edit_email_form.new_email.data.lower()
            passwd = reset_password_form.passwd.data

            if check_password_hash(user['passwd'], passwd):
                update_user_field('email', new_email, user['user_id'])
                flash('Email changed!', 'success')
                return redirect(url_for('admin.admin_profile'))
    elif reset_password_form.new_passwd.name in request.form:
        if reset_password_form.validate_on_submit():
            new_passwd = generate_password_hash(reset_password_form.new_passwd.data)
            passwd = reset_password_form.passwd.data

            if check_password_hash(user['passwd'], passwd):
                update_user_field('passwd', new_passwd, user['user_id'])
                flash('Password changed!', 'success')
                return redirect(url_for('admin.admin_profile'))

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
        return redirect(url_for('auth.user_login'))
    return render_template('admin/admin_profile.html', delete_account_form=delete_account_form)

@admin_bp.route('/admin/user-management')
@login_required(['admin'])
def user_management():
    return render_template('admin/user_management.html')

@admin_bp.route('/admin/user-profile')
@login_required(['admin'])
def user_profile():
    return render_template('admin/user_profile.html')
#SKY ADMIN ROUTES
