from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, EmailField, validators
from wtforms.validators import InputRequired, Length, EqualTo, ValidationError
from blueprints.utils import get_user_by_field

def field_exists_check(field_name):
    def _field_exists_check(form, field):
        if get_user_by_field(field_name, field.data):
            raise ValidationError(f'User with this {field_name.replace("_", " ")} already exists')
    return _field_exists_check

class RegistrationForm(FlaskForm):
    username = StringField('Username', [
    validators.InputRequired(message="Please enter a username"),
    validators.Length(min=3, max=50, message="Username must be more than 3 characters"),
    field_exists_check('username')
    ])
    phone_num = StringField('Phone Number', [
    validators.InputRequired(message="Please enter a phone number"),
    validators.Regexp(regex=r'^\d{8}$', message="Invalid phone number"),
    field_exists_check('phone_num')
    ])
    email = EmailField('Email', [
    validators.InputRequired(message="Please enter an email"),
    validators.Email(message='Invalid email'),
    field_exists_check('email')
    ])
    passwd = PasswordField('Password', [
    validators.InputRequired(message="Please enter a password"),
    validators.Length(min=8, max=64, message="Password must be more than 8 characters"),
    ])
    confirm_passwd = PasswordField('Confirm password', [
    validators.InputRequired(message="Please retype password"),
    validators.EqualTo('passwd', message='Passwords do not match')
    ])

class LoginForm(FlaskForm):
    username = StringField('Username', [
    validators.InputRequired(message="Please enter a username"),
    validators.Length(max=50)
    ])
    passwd = PasswordField('Password', [
    validators.InputRequired(message="Please enter a password"),
    validators.Length(max=64)
    ])

class MessageForm(FlaskForm):
    message = StringField('Message', [
    validators.InputRequired(message="Please enter a username"),
    validators.Length(min=1, max=160)
    ])
