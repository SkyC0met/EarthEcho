from flask import Blueprint, render_template, request, flash, redirect, url_for, current_app, session
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField
from wtforms.validators import DataRequired
import requests
from db import get_db_connection
from mysql.connector import Error
import random

class UnbanRequestForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    first_name = StringField('First Name', validators=[DataRequired()])
    last_name = StringField('Last Name', validators=[DataRequired()])
    request = TextAreaField('Unban Request', validators=[DataRequired()])
    submit = SubmitField('Submit')

unban_bp = Blueprint('unban', __name__, template_folder='templates')

# List of security questions and their corresponding answers
SECURITY_QUESTIONS = {
    'Which energy source is renewable and comes from the sun? ': 'solar energy',
    'What gas makes up the majority of Earths atmosphere? ': 'nitrogen',
    'What is Light Emitting Diode commonly known as? ': 'led',
    'What is the term for cutting down a large area of trees? ': 'deforestation',
    'What is the term for contamination of air, water, or soil by harmful chemicals or waste? ': 'pollution',
}

@unban_bp.route('/unbanreq', methods=['GET', 'POST'])
def unban_request():
    form = UnbanRequestForm()

    if request.method == 'GET':
        # Select a random security question
        security_question = random.choice(list(SECURITY_QUESTIONS.keys()))
        # Store the correct answer in session
        session['SECURITY_ANSWER'] = SECURITY_QUESTIONS[security_question]
        return render_template('user/unbanreq.html', form=form, security_question=security_question, recaptcha_site_key=current_app.config['RECAPTCHA_SITE_KEY'])

    if form.validate_on_submit():
        # Verify reCAPTCHA
        recaptcha_response = request.form.get('g-recaptcha-response')
        recaptcha_secret = current_app.config['RECAPTCHA_SECRET_KEY']
        recaptcha_verify_url = 'https://www.google.com/recaptcha/api/siteverify'
        recaptcha_data = {
            'secret': recaptcha_secret,
            'response': recaptcha_response
        }
        recaptcha_response = requests.post(recaptcha_verify_url, data=recaptcha_data)
        recaptcha_result = recaptcha_response.json()

        if not recaptcha_result.get('success'):
            flash('reCAPTCHA verification failed. Please try again.', 'danger')
            return redirect(url_for('unban.unban_request'))

        # Check security question
        security_answer = request.form.get('security_answer')
        if security_answer and security_answer.lower() == session.get('SECURITY_ANSWER', '').lower():
            # Process the form data
            username = form.username.data
            first_name = form.first_name.data
            last_name = form.last_name.data
            request_text = form.request.data

            # Save the data to the database
            conn = get_db_connection()
            cursor = conn.cursor()
            try:
                cursor.execute("""
                    INSERT INTO unban_requests (username, first_name, last_name, request)
                    VALUES (%s, %s, %s, %s)
                """, (username, first_name, last_name, request_text))
                conn.commit()
                flash('Your unban request has been submitted successfully!', 'success')
            except Error as e:
                conn.rollback()
                flash(f'An error occurred: {e}', 'danger')
            finally:
                cursor.close()
                conn.close()

            return redirect(url_for('unban.unban_request'))
        else:
            flash('Security question answer is incorrect.', 'danger')
            return redirect(url_for('unban.unban_request'))

    return render_template('user/unbanreq.html', form=form, security_question=session.get('SECURITY_QUESTION'),
                           recaptcha_site_key=current_app.config['RECAPTCHA_SITE_KEY'])