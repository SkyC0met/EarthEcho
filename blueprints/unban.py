# unban.py

from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, Email

class UnbanRequestForm(FlaskForm):
    first_name = StringField('First Name', validators=[DataRequired()])
    last_name = StringField('Last Name', validators=[DataRequired()])
    email = StringField('Email Address', validators=[DataRequired(), Email()])
    request = TextAreaField('Unban Request', validators=[DataRequired()])
    submit = SubmitField('Submit')

unban_bp = Blueprint('unban', __name__, template_folder='templates')

@unban_bp.route('/unbanreq', methods=['GET', 'POST'])
def unban_request():
    form = UnbanRequestForm()
    if form.validate_on_submit():
        # Process the form data
        first_name = form.first_name.data
        last_name = form.last_name.data
        email = form.email.data
        request_text = form.request.data

        # Here you would typically save the data to a database or send an email

        flash('Unban request submitted successfully!', 'success')
        return redirect(url_for('unban.unban_request'))

    return render_template('user/unbanreq.html', form=form)
