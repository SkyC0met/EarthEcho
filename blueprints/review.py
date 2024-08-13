from flask import Blueprint, jsonify, request, session
from datetime import datetime, timedelta
from db import get_db_connection
from blueprints.utils import get_user_by_field
import bleach

review_bp = Blueprint('review', __name__)

def sanitize_input(input_str):
    allowed_tags = ['b', 'i', 'u', 'em', 'strong', 'a']
    return bleach.clean(input_str, tags=allowed_tags)

@review_bp.route('/submit_review', methods=['POST'])
def submit_review():
    try:
        print("Received request to /submit_review")
        rating = request.form.get('rating')
        review = request.form.get('review')
        post_id = request.form.get('post_id')  # Use dynamic post_id
        user_id = session.get('_user_id')

        # Check if user is logged in
        if not user_id:
            print("User not logged in")
            return jsonify({'status': 'error', 'message': 'User not logged in'}), 401

        # Retrieve user data
        user = get_user_by_field('user_id', user_id)
        username = user['username']

        if not post_id:
            return jsonify({'status': 'error', 'message': 'Post ID is missing'}), 400

        try:
            # Convert post_id to integer
            post_id = int(post_id)
        except ValueError:
            return jsonify({'status': 'error', 'message': 'Invalid Post ID'}), 400

        # Check for missing fields
        if not rating or not review:
            print("Missing fields detected")
            return jsonify({'status': 'error', 'message': 'Please fill in both the rating and review before submitting'}), 400

        try:
            rating = int(rating)
        except ValueError:
            print("Invalid rating value detected")
            return jsonify({'status': 'error', 'message': 'Invalid rating value'}), 400

        # Sanitize review input
        review = sanitize_input(review)
        print(f"Sanitized review: {review}")

        # Check review count for today
        connection = get_db_connection()
        if connection:
            cursor = connection.cursor()
            today_start = datetime.now().date()
            today_end = today_start + timedelta(days=1)

            count_query = """
                SELECT COUNT(*) FROM review 
                WHERE user_id = %s AND timestamp >= %s AND timestamp < %s
            """
            cursor.execute(count_query, (user_id, today_start, today_end))
            review_count = cursor.fetchone()[0]

            # rate limiting
            if review_count >= 5:
                print("Daily review limit reached")
                return jsonify({'status': 'error', 'message': 'You have reached the daily review limit'}), 429

            # Insert new review
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

