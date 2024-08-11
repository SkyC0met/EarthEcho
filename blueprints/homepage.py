from flask import Blueprint, render_template, redirect, url_for, flash, session
from blueprints.utils import *

homepage_bp = Blueprint('homepage', __name__)
def get_all_posts():
    db = get_db_connection()
    cursor = db.cursor()
    cursor.execute("SELECT post_id, header, username, image_name FROM posts")
    all_posts = [dict(post_id=row[0], header=row[1], username=row[2], image_name=row[3]) for row in cursor.fetchall()]
    # Debug: Print the structure of all_posts
    print("All Posts:", all_posts)
    cursor.close()
    db.close()
    return all_posts
@homepage_bp.route('/')
def home():
    all_posts = get_all_posts()
    if current_user.is_authenticated:
        user = get_user_by_field('user_id', session['_user_id'])
        if user['acc_type'] == 'admin':
            flash("Unauthorized access.", 'danger')
            return redirect(url_for('admin.admin_profile'))
        users = get_all_users(session['_user_id'])
        return render_template('user/homepage.html', users=users, all_posts=all_posts)
    return render_template('user/homepage.html', all_posts=all_posts)

# Homepage route to fetch and display posts
@homepage_bp.route('/')
def homepage():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT * FROM posts ORDER BY created_at DESC")
    all_posts = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template('homepage.html', all_posts=all_posts)