import os
from datetime import datetime
from flask import Blueprint, flash, url_for, redirect, render_template, current_app, request, jsonify
from flask_login import login_required, current_user
from flask_wtf import FlaskForm
from werkzeug.utils import secure_filename
from wtforms import StringField, TextAreaField, SubmitField, FileField, SelectField
from wtforms.fields.datetime import DateField
from wtforms.validators import DataRequired, Length, ValidationError
from flask_wtf.file import FileAllowed
from db import get_db_connection

edit_bp = Blueprint('edit', __name__)


class EditPostForm(FlaskForm):
    header = StringField('Header', validators=[DataRequired(), Length(max=120)])
    image = FileField('Image', validators=[FileAllowed(['jpg', 'jpeg', 'png'], 'Only JPEG and PNG images are allowed')])
    topic = SelectField('Topic',
                        choices=[(1, 'Sustainability'), (2, 'Pollution'), (3, 'Recycling'), (4, 'Water/Oceans'),
                                 (5, 'DIY'), (6, 'Energy'), (7, 'Composting'), (8, 'Others')],
                        validators=[DataRequired()])
    body = TextAreaField('Body', validators=[DataRequired()])
    submit = SubmitField('Update Post')

    def validate_image(form, field):
        if field.data:
            if field.data.filename.split('.')[-1].lower() not in ['jpg', 'jpeg', 'png']:
                raise ValidationError('Only JPEG and PNG images are allowed')

@edit_bp.route('/editpost/<int:post_id>', methods=['GET', 'POST'])
@login_required
def edit_post(post_id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM posts WHERE post_id = %s", (post_id,))
    post = cursor.fetchone()
    cursor.close()
    conn.close()

    if post is None:
        flash("Post not found!", "error")
        return redirect(url_for('myposts.my_posts'))

    form = EditPostForm(
        header=post['header'],
        topic=post['topic'],
        body=post['body']
    )

    if form.validate_on_submit():
        header = form.header.data
        topic = form.topic.data
        body = form.body.data
        image = form.image.data

        if image:
            image_name = secure_filename(image.filename)
            image_path = os.path.join(current_app.config['UPLOAD_FOLDER'], image_name)
            image.save(image_path)

            with open(image_path, 'rb') as f:
                image_data = f.read()
        else:
            image_data = post['image_data']
            image_name = post['image_name']

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE posts SET header = %s, topic = %s, body = %s, image_data = %s, image_name = %s WHERE post_id = %s",
            (header, topic, body, image_data, image_name, post_id)
        )
        conn.commit()
        cursor.close()
        conn.close()

        flash("Post updated successfully!", "success")
        return redirect(url_for('view.view_post', post_id=post_id))

    return render_template('user/editpost.html', form=form, post=post)


@edit_bp.route('/delete_post/<int:post_id>', methods=['POST'])
@login_required
def delete_post(post_id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    try:
        cursor.execute("DELETE FROM posts WHERE post_id = %s", (post_id,))
        conn.commit()
        flash('Post deleted successfully!', 'success')
    except Exception as e:
        conn.rollback()
        flash('Error deleting post: ' + str(e), 'danger')
    finally:
        cursor.close()
        conn.close()

    return redirect(url_for('myposts.my_posts'))