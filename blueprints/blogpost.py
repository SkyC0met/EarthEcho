from flask import render_template, Blueprint, abort, request, jsonify, session
from db import get_db_connection
from blueprints.sky_forms import AddFavouritesForm
from blueprints.utils import *
import base64

blogpost_bp = Blueprint('bp', __name__)

@blogpost_bp.route('/post/<int:post_id>')
def post(post_id):
    add_favourites_form = AddFavouritesForm()
    is_favourite = False
    author_uuid = None  # Initialize the UUID variable

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    # Fetch post data
    cursor.execute('SELECT * FROM posts WHERE post_id = %s', (post_id,))
    post = cursor.fetchone()

    if post is None:
        abort(404)  # Handle the case where the post does not exist

    # Fetch author data
    cursor.execute('SELECT * FROM users WHERE user_id = %s', (post['user_id'],))
    author = cursor.fetchone()

    if author:
        author_uuid = author['uuid']  # Get the UUID of the author

    # Convert the image data to a base64-encoded string
    if post['image_data']:
        post['image_data'] = base64.b64encode(post['image_data']).decode('utf-8')

    # Fetch review data
    cursor.execute('''
        SELECT review, rating, timestamp, users.username
        FROM review
        JOIN users ON review.user_id = users.user_id
        WHERE post_id = %s
    ''', (post_id,))
    reviews = cursor.fetchall()

    # Convert review timestamps to strings if necessary
    for review in reviews:
        review['timestamp'] = review['timestamp'].strftime('%Y-%m-%d %H:%M:%S')

    if current_user.is_authenticated:
        user_id = session['_user_id']
        is_favourite = False
        if user_id:
            cursor.execute('''
                SELECT 1 FROM user_favourites
                WHERE user_id = %s AND post_id = %s
            ''', (user_id, post_id))
            is_favourite = cursor.fetchone() is not None

    cursor.close()
    conn.close()

    return render_template(
        'user/testpost2.html',
        post=post,
        total_reviews=len(reviews),
        reviews=reviews,
        current_page=1,
        reviews_per_page=3,
        add_favourites_form=add_favourites_form,
        is_favourite=is_favourite,
        uuid=author_uuid  # Pass the UUID to the template
    )

@blogpost_bp.route('/get_reviews', methods=['GET'])
def get_reviews():
    post_id = request.args.get('post_id', type=int)
    page = request.args.get('page', default=1, type=int)
    limit = request.args.get('limit', default=3, type=int)

    if not post_id:
        return jsonify({'error': 'Post ID is required'}), 400

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    # Calculate offset
    offset = (page - 1) * limit

    cursor.execute('''
        SELECT review, rating, timestamp, users.username
        FROM review
        JOIN users ON review.user_id = users.user_id
        WHERE post_id = %s
        ORDER BY timestamp DESC
        LIMIT %s OFFSET %s
    ''', (post_id, limit, offset))
    reviews = cursor.fetchall()

    cursor.execute('''
        SELECT COUNT(*) AS total_reviews
        FROM review
        WHERE post_id = %s
    ''', (post_id,))
    total_reviews = cursor.fetchone()['total_reviews']

    # Calculate average rating and rating distribution
    cursor.execute('''
        SELECT AVG(rating) AS average_rating
        FROM review
        WHERE post_id = %s
    ''', (post_id,))
    average_rating = cursor.fetchone()['average_rating']

    cursor.execute('''
        SELECT rating, COUNT(*) AS count
        FROM review
        WHERE post_id = %s
        GROUP BY rating
    ''', (post_id,))
    rating_distribution = [0, 0, 0, 0, 0]  # Initialize for 1 to 5 stars
    for row in cursor.fetchall():
        rating_distribution[row['rating'] - 1] = row['count']

    cursor.close()
    conn.close()

    return jsonify({
        'reviews': reviews,
        'total_reviews': total_reviews,
        'average_rating': average_rating,
        'rating_distribution': rating_distribution
    })
