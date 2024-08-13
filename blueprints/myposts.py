import base64
from flask import Blueprint, render_template, session
from flask_login import login_required
from blueprints.sky_forms import SearchbarForm

from db import get_db_connection

myposts_bp = Blueprint('myposts', __name__)

@myposts_bp.route('/my_posts', methods=['GET'])
@login_required
def my_posts():
    searchbar_form = SearchbarForm()
    # Get the current user's ID
    user_id = session['_user_id']
    print("User ID:", user_id)  # Add this line

    # Retrieve all posts made by the current user, ordered by most recent first
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT post_id, header, image_data FROM posts WHERE user_id = %s ORDER BY timestamp DESC",
        (session['_user_id'],)
    )
    posts = cursor.fetchall()  # Fetch all the results
    cursor.close()
    conn.close()

    # Convert the image data to base64-encoded strings
    posts_with_base64_images = []
    for post in posts:
        post_id, header, image_data = post
        base64_image = base64.b64encode(image_data).decode('utf-8')
        posts_with_base64_images.append((post_id, header, base64_image))

    return render_template('user/myposts.html', posts=posts_with_base64_images, searchbar_form=searchbar_form)