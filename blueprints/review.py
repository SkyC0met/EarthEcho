from flask import Blueprint, jsonify, request, session, render_template
from datetime import datetime
from db import get_db_connection
from blueprints.utils import get_user_by_field

review_bp = Blueprint('review', __name__)

# @review_bp.route('/submit_review', methods=['POST'])
# def submit_review():
#     return jsonify({
#         'status': 'success',
#         'date': datetime.now().strftime('%Y-%m-%d'),
#         'time': datetime.now().strftime('%H:%M:%S'),
#         'review': 'Test review'
#     }), 200


@review_bp.route('/submit_review', methods=['POST'])
def submit_review():
    try:
        print("Received request to /submit_review")

        rating = request.form.get('rating')
        review = request.form.get('review')
        post_id = 1
        user = get_user_by_field('user_id', session['_user_id'])
        username = user['username']

        print(f"Retrieved form data - Rating: {rating}, Review: {review}, Post ID: {post_id}")

        if not rating or not review or not post_id:
            print("Missing fields detected")
            return jsonify({'status': 'error', 'message': 'Missing fields'}), 400

        try:
            rating = int(rating)
        except ValueError:
            print("Invalid rating value detected")
            return jsonify({'status': 'error', 'message': 'Invalid rating value'}), 400

        user_id = session.get('_user_id')
        if not user_id:
            print("User not logged in")
            return jsonify({'status': 'error', 'message': 'User not logged in'}), 401

        connection = get_db_connection()
        if connection:
            cursor = connection.cursor()
            now = datetime.now()
            insert_query = "INSERT INTO review (review, rating, post_id, user_id, timestamp) VALUES (%s, %s, %s, %s, %s)"
            cursor.execute(insert_query, (review, rating, post_id, user_id, now))
            connection.commit()

            response_data = {
                'status': 'success',
                'timestamp': now.strftime('%Y-%m-%d %H:%M:%S'),
                'review': review,
                'rating': rating,
                'username': username
            }

            return jsonify(response_data), 200

    except Exception as e:
        print(f"Unexpected Error: {e}")
        return jsonify({'status': 'error', 'message': 'An unexpected error occurred'}), 500

    finally:
        if 'connection' in locals() and connection.is_connected():
            cursor.close()
            connection.close()
            print("Connection closed")

    return jsonify({'status': 'error', 'message': 'Unknown error occurred'}), 400


@review_bp.route('/get_reviews', methods=['GET'])
def get_reviews():
    post_id = 1  # static
    page = int(request.args.get('page', 1))
    limit = int(request.args.get('limit', 3))
    offset = (page - 1) * limit

    connection = None
    cursor = None
    reviews = []
    avg_rating = 0
    review_count = 0
    rating_distribution = [0] * 5

    try:
        connection = get_db_connection()
        if not connection:
            return jsonify({'error': 'Database connection failed'}), 500

        cursor = connection.cursor()

        # Fetch reviews
        query = """
            SELECT r.review, r.rating, r.timestamp, u.username
            FROM review r
            JOIN users u ON r.user_id = u.user_id
            WHERE r.post_id = %s
            ORDER BY r.timestamp DESC
            LIMIT %s OFFSET %s
        """
        cursor.execute(query, (post_id, limit, offset))
        reviews = cursor.fetchall()

        # Check if more reviews exist
        cursor.execute("SELECT COUNT(*) FROM review WHERE post_id = %s", (post_id,))
        total_reviews = cursor.fetchone()[0]

        # Calculate average rating
        avg_query = "SELECT AVG(rating) FROM review WHERE post_id = %s"
        cursor.execute(avg_query, (post_id,))
        avg_rating_result = cursor.fetchone()
        if avg_rating_result:
            avg_rating = avg_rating_result[0]

        # Rating distribution
        dist_query = "SELECT rating, COUNT(*) FROM review WHERE post_id = %s GROUP BY rating"
        cursor.execute(dist_query, (post_id,))
        distribution = cursor.fetchall()
        for rating, count in distribution:
            rating_distribution[rating - 1] = count

        return jsonify({
            'reviews': [{'username': r[3], 'timestamp': r[2].strftime('%Y-%m-%d %H:%M:%S'), 'rating': r[1], 'review': r[0]} for r in reviews],
            'average_rating': avg_rating,
            'total_reviews': total_reviews,
            'rating_distribution': rating_distribution
        })

    except Exception as e:
        print(f"Unexpected Error: {e}")
        return jsonify({'error': 'An unexpected error occurred'}), 500

    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()
