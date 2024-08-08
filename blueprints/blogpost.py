from flask import render_template, Blueprint, abort
from db import get_db_connection

blogpost_bp = Blueprint('bp', __name__)

@blogpost_bp.route('/post/<int:post_id>')
def post(post_id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    # Fetch post data
    cursor.execute('SELECT * FROM posts WHERE post_id = %s', (post_id,))
    post = cursor.fetchone()

    # Fetch author data
    cursor.execute('SELECT * FROM users WHERE user_id = %s', (post['user_id'],))
    author = cursor.fetchone()

    cursor.close()
    conn.close()
    # Convert the image data to a base64-encoded string
    if post['image_data']:
        import base64
        post['image_data'] = base64.b64encode(post['image_data']).decode('utf-8')

    if post is None:
        abort(404)  # Handle the case where the post does not exist

    return render_template('user/testpost2.html', post=post)

