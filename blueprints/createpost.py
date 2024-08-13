import os
from datetime import date, datetime
from flask import Blueprint, flash, url_for, redirect, render_template, current_app, Flask, session
from flask_login import login_required, current_user
from flask_wtf import FlaskForm
from werkzeug.utils import secure_filename
from wtforms import StringField, TextAreaField, SubmitField, FileField, SelectField
from wtforms.fields.datetime import DateField
from wtforms.validators import DataRequired, Length, ValidationError
from flask_wtf.file import FileAllowed
from db import get_db_connection

create_bp = Blueprint('create', __name__)
class PostForm(FlaskForm):
    username = StringField('Username', render_kw={'readonly': True})
    date_created = DateField('Date', default=date.today, render_kw={'readonly': True})
    header = StringField('Header', validators=[DataRequired(), Length(max=120)])
    image = FileField('Image', validators=[DataRequired()])
    topic = SelectField('Topic', choices=[('Sustainability', 'Sustainability'), ('Pollution', 'Pollution'), ('Recycling', 'Recycling'), ('Water/Oceans', 'Water/Oceans'), ('DIY', 'DIY'), ('Energy', 'Energy'), ('Composting', 'Composting'), ('Others', 'Others')], validators=[DataRequired()])
    body = TextAreaField('Body', validators=[DataRequired(), Length(min=120)])
    submit = SubmitField('Post!')

    def validate_image(form, field):
        if field.data:
            if field.data.filename.split('.')[-1].lower() not in ['jpg', 'jpeg', 'png']:
                raise ValidationError('Only JPEG and PNG images are allowed')

@create_bp.route('/createpost', methods=['GET', 'POST'])
@login_required
def create_post():
    form = PostForm()
    if form.username.data is None:
        form.username.data = current_user.username
    if form.validate_on_submit():
        user_id = session['_user_id']
        username = form.username.data
        date_created = datetime.now()
        header = form.header.data
        image = form.image.data
        topic = form.topic.data
        body = form.body.data

        # Save image to database
        image_name = secure_filename(image.filename)
        image_path = os.path.join(current_app.config['UPLOAD_FOLDER'], image_name)
        image.save(image_path)

        # Read the image data
        with open(image_path, 'rb') as f:
            image_data = f.read()

        # Save data to database
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO posts (user_id, username, header, topic, body, timestamp, image_data, image_name) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)",
            (user_id, username, header, topic, body, date_created, image_data, image_name)
        )
        conn.commit()
        cursor.close()
        conn.close()

        flash("Post created!", "success")
        return redirect(url_for('myposts.my_posts'))
    return render_template('user/createpost.html', form=form)
