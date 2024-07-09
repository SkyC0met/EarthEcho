# review.py
from flask import Blueprint, jsonify, request
from wtforms.fields import datetime
from datetime import datetime

from db import get_db_connection

review_bp = Blueprint('review', __name__)

# def check_connection():
#     try:
#         conn = get_db_connection()
#
#         if conn.is_connected():
#             print("Database connected successfully")
#             return jsonify({'status': 'success', 'message': 'Database connected successfully'})
#         else:
#             print("Database connection error")
#             return jsonify({'status': 'error', 'message': 'Database connection error'})
#
#     except Exception as e:
#         print(f"Unexpected Error: {e}")
#         return jsonify({'status': 'error', 'message': 'An unexpected error occurred'})


@review_bp.route('/submit_review', methods=['POST'])
def submit_review():
    try:
        rating = int(request.form.get('rating_hidden'))
        review = request.form.get('review')
        post_id = 1

        if not rating or not review or not post_id:
            raise ValueError("Rating, review, or post_id is missing")

        # Get user_id based on session or authentication (replace with your actual logic)
        user_id = get_current_user_id()  # Example function to retrieve current user's ID

        # Connect to your MySQL database
        connection = get_db_connection()

        if connection:
            cursor = connection.cursor()

            insert_query = "INSERT INTO review (review, rating, post_id, user_id) VALUES (%s, %s, %s, %s)"
            cursor.execute(insert_query, (review, rating, post_id, user_id))
            connection.commit()

            # Construct JSON response
            response_data = {
                'status': 'success',
                'date': datetime.now().strftime('%Y-%m-%d'),  # Current date in YYYY-MM-DD format
                'time': datetime.now().strftime('%H:%M:%S'),  # Current time in HH:MM:SS format
                'review': review  # Pass the review content back if needed
            }

            return jsonify(response_data)

    except ValueError as ve:
        print(f"ValueError: {ve}")
        return jsonify({'status': 'error', 'message': str(ve)})

    except Exception as e:
        print(f"Unexpected Error: {e}")
        return jsonify({'status': 'error', 'message': 'An unexpected error occurred'})

    finally:
        if 'connection' in locals() and connection and connection.is_connected():
            cursor.close()
            connection.close()
            print("Connection closed")

    # If an error occurs or if the submission fails, return an error response
    return jsonify({'status': 'error', 'message': 'Unknown error occurred'})

def get_current_user_id():
    # Replace this function with your actual logic to get the current user's ID
    # For example, if using Flask session:
    # return session.get('user_id')
    # Or if using authentication:
    # return current_user.id
    # For demo purposes, return a static user_id (replace with actual logic)
    return 1  # Example: Replace with actual logic to get current user ID dynamically

