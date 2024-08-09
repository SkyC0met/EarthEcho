import html
import os

from flask import Blueprint, request, jsonify, render_template, flash, url_for, redirect, abort, session
from werkzeug.utils import secure_filename
from wtforms.fields import datetime
from datetime import datetime

from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField, FileField, SelectField
from wtforms.validators import DataRequired, Length
from flask_wtf.file import FileAllowed

from blueprints.chatbot.chat import get_response
from db import get_db_connection
from blueprints.sky_forms import AddFavouritesForm

init_bp = Blueprint('init', __name__)

@init_bp.route('/game')
def game():
    return render_template('game/First Game.html')

# chatbot
@init_bp.post("/predict")
def predict():
    text = request.get_json().get("message")
    sanitized_text = html.escape(text)
    response = get_response(sanitized_text)
    message = {"answer": response}
    return jsonify(message)

# # @init_bp.route('/Blog')
# # def blog():
# #     return render_template('user/blogpost.html')
@init_bp.route('/Blog')
def blog():
    post_id = 1  # static
    current_page = 1
    reviews_per_page = 3
    total_reviews = 0
    reviews = []

    connection = None
    cursor = None
    try:
        connection = get_db_connection()
        if not connection:
            print("Database connection failed.")
            return render_template('user/blogpost.html', reviews=reviews, current_page=current_page, reviews_per_page=reviews_per_page, total_reviews=total_reviews)

        cursor = connection.cursor()

        # Get total number of reviews
        cursor.execute("SELECT COUNT(*) FROM review WHERE post_id = %s", (post_id,))
        total_reviews = cursor.fetchone()[0]

        # Fetch reviews
        query = """
            SELECT r.review, r.rating, r.timestamp, u.username
            FROM review r
            JOIN users u ON r.user_id = u.user_id
            WHERE r.post_id = %s
            ORDER BY r.timestamp DESC
            LIMIT %s OFFSET %s
        """
        offset = (current_page - 1) * reviews_per_page
        cursor.execute(query, (post_id, reviews_per_page, offset))
        reviews = cursor.fetchall()

        is_favourite = False
        user_id = session.get('_user_id')

        # Check if the post is in user's favourites
        cursor.execute("SELECT COUNT(*) FROM user_favourites WHERE user_id = %s AND post_id = %s", (user_id, post_id))
        is_favourite = cursor.fetchone()[0] > 0

    except Exception as e:
        print(f"Unexpected Error: {e}")

    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()

    add_favourites_form = AddFavouritesForm()
    return render_template('user/blogpost.html', reviews=reviews, current_page=current_page, reviews_per_page=reviews_per_page, total_reviews=total_reviews, add_favourites_form=add_favourites_form, is_favourite=is_favourite)
