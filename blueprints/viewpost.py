import os
from flask import Blueprint, render_template, abort
import mysql.connector
from flask_login import login_required
from flask_wtf import FlaskForm

from db import get_db_connection

view_bp = Blueprint('view', __name__)


def get_post(post_id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM posts WHERE post_id = %s", (post_id,))
    post = cursor.fetchone()
    cursor.close()
    conn.close()
    # Convert the image data to a base64-encoded string
    if post['image_data']:
        import base64
        post['image_data'] = base64.b64encode(post['image_data']).decode('utf-8')

    return post


@view_bp.route('/view_post/<int:post_id>', methods=['GET'])
@login_required
def view_post(post_id):
    # Retrieve the post data from the database
    post = get_post(post_id)

    if post is None:
        abort(404)  # Handle the case where the post is not found

    # Create an empty form for CSRF token
    form = FlaskForm()  # If needed for CSRF validation

    # Render the "View Post" page, passing the post data to the template
    return render_template('user/viewpost.html', post=post, form=form)
