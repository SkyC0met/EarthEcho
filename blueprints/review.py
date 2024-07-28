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
            insert_query = "INSERT INTO review (review, rating, post_id, user_id) VALUES (%s, %s, %s, %s)"
            cursor.execute(insert_query, (review, rating, post_id, user_id))
            connection.commit()

            response_data = {
                'status': 'success',
                'date': datetime.now().strftime('%Y-%m-%d'),
                'time': datetime.now().strftime('%H:%M:%S'),
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
    post_id = 1
    connection = None
    cursor = None
    try:
        connection = get_db_connection()
        if not connection:
            print("Database connection failed.")
            return jsonify({'error': 'Database connection failed'}), 500

        cursor = connection.cursor()
        query = """
            SELECT r.review, r.rating, r.timestamp, u.username
            FROM review r
            JOIN users u ON r.user_id = u.user_id
            WHERE r.post_id = %s
            ORDER BY r.timestamp DESC
        """
        cursor.execute(query, (post_id,))
        reviews = cursor.fetchall()

        return jsonify({'reviews': reviews})

    except Exception as e:
        print(f"Unexpected Error: {e}")
        return jsonify({'error': 'An unexpected error occurred'}), 500

    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()
