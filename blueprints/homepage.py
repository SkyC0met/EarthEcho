import base64

from flask import Blueprint, render_template, redirect, url_for, flash, session
from blueprints.utils import *

homepage_bp = Blueprint('homepage', __name__)

def get_all_posts():
    db = get_db_connection()
    cursor = db.cursor()
    cursor.execute("SELECT post_id, header, username, image_data FROM posts ORDER BY timestamp desc")

    all_posts = []
    for row in cursor.fetchall():
        post_id, header, username, image_data = row
        base64_image = None
        if image_data:
            if isinstance(image_data, str):
                image_data = image_data.encode('utf-8')  # Ensure it's in bytes
            base64_image = base64.b64encode(image_data).decode('utf-8')
        all_posts.append(dict(post_id=post_id, header=header, username=username, image_data=base64_image))

    cursor.close()
    db.close()
    return all_posts

@homepage_bp.route('/')
def home():
    all_posts = get_all_posts()
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute(
        "SELECT * FROM users")
    users = cursor.fetchall()

    cursor.close()
    conn.close()

    if current_user.is_authenticated:
        user = get_user_by_field('user_id', session['_user_id'])
        if user['acc_type'] == 'admin':
            flash("Unauthorized access.", 'danger')
            return redirect(url_for('admin.admin_profile'))
        users = get_all_users(session['_user_id'])
        return render_template('user/homepage.html', users=users, all_posts=all_posts)
    return render_template('user/homepage.html', users=users, all_posts=all_posts)