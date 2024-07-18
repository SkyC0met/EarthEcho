from flask import Blueprint, render_template, session
from blueprints.utils import get_all_users

homepage_bp = Blueprint('homepage', __name__)

@homepage_bp.route('/')
def home():
    if 'user_id' in session:
        users = get_all_users(session['user_id'])
        return render_template('user/homepage.html', users=users)
    return render_template('user/homepage.html')