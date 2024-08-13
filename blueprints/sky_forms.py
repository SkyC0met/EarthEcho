from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, EmailField, HiddenField, SubmitField, BooleanField, validators
from wtforms.validators import ValidationError
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
        validators.Length(min=8, max=64, message="Password must be more than 8 characters")
    ])
    confirm_passwd = PasswordField('Confirm password', [
        validators.InputRequired(message="Please retype password"),
        validators.EqualTo('passwd', message='Passwords do not match')
    ])

class LoginForm(FlaskForm):
    username_or_email = StringField('Username or Email', [
        validators.InputRequired(message="Please enter a username or email"),
        validators.Length(max=50)
    ])
    passwd = PasswordField('Password', [
        validators.InputRequired(message="Please enter a password"),
        validators.Length(max=64)
    ])
    remember_me = BooleanField('Remember Me')

class OTPForm(FlaskForm):
    otp = StringField('OTP', [
        validators.InputRequired(message="Please enter an otp"),
        validators.Length(max=6)
    ])

class ForgotPasswordForm(FlaskForm):
    username = StringField('Username', [
        validators.InputRequired(message="Please enter your username"),
        validators.Length(min=3, max=50, message="Username must be more than 3 characters")
    ])
    email = EmailField('Email', [
        validators.InputRequired(message="Please enter your email"),
        validators.Email(message='Invalid email'),
    ])

class SearchbarForm(FlaskForm):
    search = StringField('Search', [
        validators.InputRequired(message="Please enter a message"),
        validators.Length(min=1, max=160)
    ])

class MessageForm(FlaskForm):
    receiver = HiddenField('Receiver', [
        validators.InputRequired()
    ])
    message = StringField('Message', [
        validators.InputRequired(message="Please enter a message"),
        validators.Length(min=1, max=100)
    ])

class EditUsernameForm(FlaskForm):
    new_username = StringField('New Username', [
        validators.InputRequired(message="Please enter a new username"),
        validators.Length(min=3, max=50, message="Username must be more than 3 characters")
    ])
    passwd = PasswordField('Password', [
        validators.InputRequired(message="Please enter your current password"),
        validators.Length(max=64)
    ])

class EditPhoneNumForm(FlaskForm):
    new_phone_num = StringField('New Phone Number', [
        validators.InputRequired(message="Please enter a new phone number"),
        validators.Regexp(regex=r'^\d{8}$', message="Invalid phone number"),
    ])
    passwd = PasswordField('Password', [
        validators.InputRequired(message="Please enter your current password"),
        validators.Length(max=64)
    ])

class EditEmailForm(FlaskForm):
    new_email = StringField('New Email', [
        validators.InputRequired(message="Please enter an email"),
        validators.Email(message='Invalid email')
    ])
    passwd = PasswordField('Password', [
        validators.InputRequired(message="Please enter your current password"),
        validators.Length(max=64)
    ])

class ResetPasswordForm(FlaskForm):
    passwd = PasswordField('Current Password', [
        validators.InputRequired(message="Please enter your current password"),
        validators.Length(max=64)
    ])
    new_passwd = PasswordField('New Password', [
        validators.InputRequired(message="Please enter a new password"),
        validators.Length(min=8, max=64, message="Password must be more than 8 characters")
    ])
    confirm_new_passwd = PasswordField('Retype New Password', [
        validators.InputRequired(message="Please retype your new password"),
        validators.EqualTo('new_passwd', message='Passwords do not match')
    ])

class DeleteAccountForm(FlaskForm):
    submit = SubmitField('Delete Account')

class RedeemVoucherForm(FlaskForm):
    reward_id = HiddenField('Reward ID')
    submit = SubmitField('Redeem Voucher')

class SpendVoucherForm(FlaskForm):
    submit = SubmitField('Spend Voucher')

class AddFavouritesForm(FlaskForm):
    post_id = HiddenField('post_id')
    submit = SubmitField('Add Favourite')

class AddPointsForm(FlaskForm):
    submit = SubmitField('Add Points')

class BanUserForm(FlaskForm):
    csrf_token = HiddenField()