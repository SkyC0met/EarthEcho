from flask import Blueprint, render_template, redirect, url_for, flash, session
from blueprints.utils import *

homepage_bp = Blueprint('homepage', __name__)

@homepage_bp.route('/')
def home():
    if current_user.is_authenticated:
        user = get_user_by_field('user_id', session['_user_id'])
        if user['acc_type'] == 'admin':
            flash("Unauthorized access.", 'danger')
            return redirect(url_for('admin.admin_profile'))
        users = get_all_users(session['_user_id'])
        return render_template('user/homepage.html', users=users)
    return render_template('user/homepage.html')