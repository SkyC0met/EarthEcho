from flask import Blueprint, render_template, session, redirect, url_for, flash
from blueprints.utils import get_all_users, get_user_by_field

homepage_bp = Blueprint('homepage', __name__)

@homepage_bp.route('/')
def home():
    if 'user_id' in session:
        user = get_user_by_field('user_id', session['user_id'])
        if user['acc_type'] == 'admin':
            flash("Unauthorized access.", 'danger')
            return redirect(url_for('admin.admin_profile'))
        users = get_all_users(session['user_id'])
        return render_template('user/homepage.html', users=users)
    return render_template('user/homepage.html')
