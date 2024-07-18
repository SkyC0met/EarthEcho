from flask import Blueprint, render_template, flash, redirect, url_for, session, request
from werkzeug.security import generate_password_hash, check_password_hash
from db import get_db_connection
from blueprints.utils import get_user_by_field, login_required
from blueprints.sky_forms import EditUsernameForm, EditPhoneNumForm, EditEmailForm, ResetPasswordForm, DeleteAccountForm

profile_bp = Blueprint('profile', __name__)

def update_user_field(field_name: str, field_value, user_id: int):
    conn = get_db_connection()
    cursor = conn.cursor()
    query = f"UPDATE users SET {field_name} = %s WHERE user_id = %s"
    cursor.execute(query, (field_value, user_id))
    conn.commit()
    cursor.close()
    conn.close()

def handle_edit_form(form, user, field_name, field_value_key, message):
    if form.validate_on_submit():
        new_value = getattr(form, field_value_key).data
        passwd = form.passwd.data

        if get_user_by_field(field_name, new_value):
            flash(f'{field_name.replace("_", " ").capitalize()} already exists', 'warning')
        elif check_password_hash(user['passwd'], passwd):
            update_user_field(field_name, new_value, user['user_id'])
            session[field_name] = new_value
            flash(f'{message}', 'success')
            return True
        else:
            flash('Incorrect password. Please try again.', 'danger')
    return False

def delete_account(user_id: int):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    user = get_user_by_field('user_id', session['user_id'])

    if user:
        user_id = user['user_id']

        cursor.execute("DELETE FROM users WHERE user_id = %s", (user_id,))
        cursor.execute("UPDATE users SET user_id = user_id - 1 WHERE user_id > %s", (user_id,))
        cursor.execute("DELETE FROM messages WHERE sender_user_id = %s OR receiver_user_id = %s", (user_id, user_id))
        cursor.execute("DELETE FROM posts WHERE user_id = %s", (user_id,))
        cursor.execute("DELETE FROM review WHERE user_id = %s", (user_id,))
        
        conn.commit()
        cursor.close()
        conn.close()
    else:
        cursor.close()
        conn.close()
        raise ValueError("User not found with user_id {}".format(user_id))

@profile_bp.route('/user/profile', methods=['GET', 'POST'])
@login_required(['user'])
def my_profile():
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
        if edit_email_form.validate_on_submit():
            new_email = edit_email_form.new_email.data.lower()
            passwd = reset_password_form.passwd.data

            if check_password_hash(user['passwd'], passwd):
                update_user_field('email', new_email, user['user_id'])
                flash('Email changed!', 'success')
                return redirect(url_for('profile.my_profile'))
    elif reset_password_form.new_passwd.name in request.form:
        if reset_password_form.validate_on_submit():
            new_passwd = generate_password_hash(reset_password_form.new_passwd.data)
            passwd = reset_password_form.passwd.data

            if check_password_hash(user['passwd'], passwd):
                update_user_field('passwd', new_passwd, user['user_id'])
                flash('Password changed!', 'success')
                return redirect(url_for('profile.my_profile'))

    return render_template('user/my_profile.html', user=user, edit_username_form=edit_username_form, edit_phone_num_form=edit_phone_num_form, edit_email_form=edit_email_form, reset_password_form=reset_password_form, delete_account_form=delete_account_form)

@profile_bp.route('/user/profile/delete', methods=['POST'])
@login_required(['user'])
def delete_profile():
    delete_account_form = DeleteAccountForm()
    if delete_account_form.validate_on_submit():
        user_id = session['user_id']
        delete_account(user_id)
        session.clear()
        flash('Account successfully deleted.', 'success')
        return redirect(url_for('auth.user_login'))
    return render_template('user/my_profile.html', delete_account_form=delete_account_form)