from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, Email
from mysql.connector import Error
from blueprints.utils import *

class UnbanRequestForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    first_name = StringField('First Name', validators=[DataRequired()])
    last_name = StringField('Last Name', validators=[DataRequired()])
    request = TextAreaField('Unban Request', validators=[DataRequired()])
    submit = SubmitField('Submit')

unban_bp = Blueprint('unban', __name__, template_folder='templates')

@unban_bp.route('/unbanreq', methods=['GET', 'POST'])
def unban_request():
    form = UnbanRequestForm()
    if form.validate_on_submit():
        # Process the form data
        username = form.username.data
        first_name = form.first_name.data
        last_name = form.last_name.data
        request_text = form.request.data

        # Here you save the data to a database
        conn = get_db_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("""
                INSERT INTO unban_requests (username, first_name, last_name, request)
                VALUES (%s, %s, %s, %s)
            """, (username, first_name, last_name, request_text))
            conn.commit()
        except Error as e:
            conn.rollback()
            flash(f'An error occurred: {e}', 'danger')
        finally:
            cursor.close()
            conn.close()

        return redirect(url_for('unban.unban_request'))

    return render_template('user/unbanreq.html', form=form)
