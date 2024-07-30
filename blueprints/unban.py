from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, Email
import mysql.connector
from mysql.connector import Error

class UnbanRequestForm(FlaskForm):
    user_id = StringField('User ID', validators=[DataRequired()])
    first_name = StringField('First Name', validators=[DataRequired()])
    last_name = StringField('Last Name', validators=[DataRequired()])
    email = StringField('Email Address', validators=[DataRequired(), Email()])
    request = TextAreaField('Unban Request', validators=[DataRequired()])
    submit = SubmitField('Submit')

unban_bp = Blueprint('unban', __name__, template_folder='templates')

def create_connection():
    """ create a database connection to the MySQL database """
    connection = None
    try:
        connection = mysql.connector.connect(
            host='localhost',
            database='earthecho_db',
            user='your_username',
            password='your_password'
        )
    except Error as e:
        print(f"Error: '{e}'")
    return connection

@unban_bp.route('/unbanreq', methods=['GET', 'POST'])
def unban_request():
    form = UnbanRequestForm()
    if form.validate_on_submit():
        # Process the form data
        user_id = form.user_id.data
        first_name = form.first_name.data
        last_name = form.last_name.data
        email = form.email.data
        request_text = form.request.data

        # Here you save the data to a database
        connection = create_connection()
        cursor = connection.cursor()
        try:
            cursor.execute("""
                INSERT INTO unban_requests (user_id, first_name, last_name, email, request)
                VALUES (%s, %s, %s, %s)
            """, (user_id, first_name, last_name, email, request_text))
            connection.commit()
            flash('Unban request submitted successfully!', 'success')
        except Error as e:
            connection.rollback()
            flash(f'An error occurred: {e}', 'danger')
        finally:
            cursor.close()
            connection.close()

        return redirect(url_for('unban.unban_request'))

    return render_template('user/unbanreq.html', form=form)
