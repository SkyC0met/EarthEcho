import os
from flask import Blueprint, render_template, abort
import mysql.connector
from flask_login import login_required

from db import get_db_connection

view_bp = Blueprint('view', __name__)


def get_post(post_id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM posts WHERE post_id = %s", (post_id,))
    post = cursor.fetchone()
    cursor.close()
    conn.close()
    return post


@view_bp.route('/view_post/<int:post_id>', methods=['GET'])
@login_required
def view_post(post_id):
    # Retrieve the post data from the database
    post = get_post(post_id)

    if post is None:
        abort(404)  # Handle the case where the post is not found

    # Render the "View Post" page, passing the post data to the template
    return render_template('user/viewpost.html', post=post)
