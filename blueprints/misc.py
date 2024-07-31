from flask import render_template, Blueprint, session
from blueprints.utils import *
from flask_login import login_required

misc_bp = Blueprint('misc', __name__)

@misc_bp.app_errorhandler(404)
# Page not found
def four_o_four(e):
    if '_user_id' in session:
        user = get_user_by_field('user_id', session['_user_id'])
        if user['acc_type'] == 'admin':
            return render_template('misc/admin_404.html'), 404
        else:
            return render_template('misc/user_404.html'), 404
    else:
        return render_template('misc/user_404.html'), 404

@misc_bp.app_errorhandler(500)
# Internal server error
def five_o_o(e):
    return render_template('misc/500.html'), 500

# Route to simulate a 500 error
@misc_bp.route('/error')
def error():
    # This will deliberately raise an exception to simulate a 500 error
    # <a href="{{ url_for('homepage') }}">Hello</a>
    raise Exception("This is a simulated 500 error")

@misc_bp.route('/1')
def one():
    return render_template('misc/1.html')

@misc_bp.route('/2')
@login_required
def two():
    return render_template('misc/2.html')

@misc_bp.route('/css')
def css():
    return render_template('misc/check_css.html')