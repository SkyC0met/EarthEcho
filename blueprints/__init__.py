import html
import os

from flask import Blueprint, request, jsonify, render_template, flash, url_for, redirect, abort
from werkzeug.utils import secure_filename
from wtforms.fields import datetime
from datetime import datetime

from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField, FileField, SelectField
from wtforms.validators import DataRequired, Length
from flask_wtf.file import FileAllowed

from blueprints.chatbot.chat import get_response
from db import get_db_connection

init_bp = Blueprint('init', __name__)

def Posts():
    posts = [
        {
            'id': 1,
            'title': 'How to be sustainable?',
            'text': 'lorem ipsum adhdyj gdh gsshh hu gdh gsh asgasd sdivvvvFVUvjusd cgibsdjhbcu',
            'author': 'John Doe',
            'date_created': '23-01-2024',
            'topic': 'Sustainability',
            'image': 'static/images/electricity.jpg'
        },
        {
            'id': 2,
            'title': 'Littering and its effects.',
            'text': 'lorem ipsum adhdyj gdh gsshh hu gdh gsh asgasd sdivvvvFVUvjusd cgibsdjhbcu',
            'author': 'John Doe',
            'date_created': '25-01-2024',
            'topic': 'Pollution',
            'image': 'static/images/electricity.jpg'

        },
        {
            'id': 3,
            'title': 'Conserving Energy!',
            'text': 'lorem ipsum adhdyj gdh gsshh hu gdh gsh asgasd sdivvvvFVUvjusd cgibsdjhbcu',
            'author': 'John Doe',
            'date_created': '26-01-2024',
            'topic': 'Electricity',
            'image': 'static/images/electricity.jpg'

        }
    ]
    return posts

Posts = Posts()

class PostForm(FlaskForm):
    author = "John Doe"
    header = StringField('Header', validators=[DataRequired() , Length(min=1, max=120)])
    body = TextAreaField('Body', validators=[DataRequired(), Length(min=1)])
    topic = SelectField('Topic', choices=[('Sustainability', "Sustainability"), ('Electricity', "Electricity"),('Pollution','Pollution'), ('recycling', 'recycling')])
    image = FileField('Image', validators=[DataRequired(),FileAllowed(['jpg', 'png'])])
    submit = SubmitField('Post!')

# chatbot
@init_bp.post("/predict")
def predict():
    text = request.get_json().get("message")
    sanitized_text = html.escape(text)
    response = get_response(sanitized_text)
    message = {"answer": response}
    return jsonify(message)

# @init_bp.route('/Blog')
# def blog():
#     return render_template('user/blogpost.html')
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

    except Exception as e:
        print(f"Unexpected Error: {e}")

    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()

    return render_template('user/blogpost.html', reviews=reviews, current_page=current_page, reviews_per_page=reviews_per_page, total_reviews=total_reviews)

@init_bp.route('/createpost', methods=['GET', 'POST'])
def CreatePosts():
    form = PostForm()
    if form.validate_on_submit():
        author = "John Doe"
        title = form.title.data
        text = form.text.data
        topic = form.topic.data
        image = form.image.data
        filename = secure_filename(image.filename)
        if filename:
            image.save(os.path.join('static/images', filename))
            image_path = os.path.join('static/images', filename)
        new_post = {
            'id': len(Posts) + 1,
            'title': title,
            'text': text,
            'author': author,
            'date_created': datetime.now().strftime('%d-%m-%Y'),
            'topic': topic,
        }
        Posts.append(new_post)
        flash("Post created!", "success")
        return redirect(url_for('init.MyPosts'))
    return render_template("user/createpost.html", form=form)

@init_bp.route('/myposts')
def MyPosts():
    return render_template('user/myposts.html', Posts = Posts)

@init_bp.route('/myposts/<int:id>/')
def ViewPost(id):
    post = next((post for post in Posts if post['id'] == id), None)
    if post is None:
        abort(404)  # Return a 404 error if the post is not found
    return render_template('user/viewpost.html', post=post)