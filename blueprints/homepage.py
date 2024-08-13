import base64
from flask import Blueprint, render_template, redirect, url_for, flash, session, request
from blueprints.utils import *
from blueprints.rate_limiter import *
from blueprints.sky_forms import SearchbarForm

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

MAX_QUERY_LENGTH = 100
def sanitize_input(input_string):
    return ''.join(c for c in input_string if c.isalnum() or c.isspace())

@homepage_bp.route('/')
def home():
    all_posts = get_all_posts()
    searchbar_form = SearchbarForm()

    if current_user.is_authenticated:
        user = get_user_by_field('user_id', session['_user_id'])
        if user['acc_type'] == 'admin':
            flash("Unauthorized access.", 'danger')
            return redirect(url_for('admin.admin_profile'))
        return render_template('user/homepage.html', all_posts=all_posts, searchbar_form=searchbar_form)
    return render_template('user/homepage.html', all_posts=all_posts, searchbar_form=searchbar_form)

@homepage_bp.route('/search', methods=['POST'])
def search():
    searchbar_form = SearchbarForm()
    if searchbar_form.validate_on_submit():
        query = searchbar_form.search.data
        query = sanitize_input(query)

        if len(query) > MAX_QUERY_LENGTH:
            flash("Your search query is too long.", "danger")
            return redirect(url_for('homepage.home'))
    
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM posts WHERE header LIKE %s", (f"%{query}%",))
        results = cursor.fetchall()
        for result in results:
            if result['image_data']:
                result['image_data'] = base64.b64encode(result['image_data']).decode('utf-8')
        cursor.close()
        conn.close()

    return render_template('user/search_results.html', results=results, query=query, searchbar_form=searchbar_form)