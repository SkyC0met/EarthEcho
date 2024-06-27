import os
import mysql.connector

from flask import Flask, request, jsonify, render_template, flash, url_for, redirect, abort
from werkzeug.utils import secure_filename
from wtforms.fields import datetime
from datetime import datetime

from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField, FileField, SelectField
from wtforms.validators import DataRequired, Length
from flask_wtf.file import FileAllowed

from chat import get_response
from racheldb import connect_and_fetch

app = Flask(__name__)
app.config['SECRET_KEY'] = 'rzstxrdycfuvgibhnj'


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
    title = StringField('Title', validators=[DataRequired() , Length(min=1, max=100)])
    text = TextAreaField('Text', validators=[DataRequired()])
    topic = SelectField('Topic', choices=[('Sustainability', "Sustainability"), ('Electricity', "Electricity"),('Pollution','Pollution'), ('recycling', 'recycling')])
    image = FileField('Image', validators=[DataRequired(),FileAllowed(['jpg', 'png'])])
    submit = SubmitField('Post!')


# chatbot
@app.post("/predict")
def predict():
    text = request.get_json().get("message")
    response = get_response(text)
    message = {"answer": response}
    return jsonify(message)

# rating and review
@app.route('/submit_review', methods=['POST'])
def submit_review():
    try:
        rating = request.form.get('rating_hidden')
        review = request.form.get('review')

        if not rating or not review:
            raise ValueError("Rating or review is missing")

        user_id = 10  # Replace with actual user ID logic if needed
        post_id = 1  # Replace with actual post ID logic if needed

        connection = connect_and_fetch()  # Connect to your MySQL database

        if connection:
            cursor = connection.cursor()

            insert_query = "INSERT INTO ratings_reviews (rating, reviews, post_id, user_id) VALUES (%s, %s, %s, %s)"
            cursor.execute(insert_query, (rating, review, post_id, user_id))
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

    except mysql.connector.Error as err:
        print(f"MySQL Error: {err}")
        return jsonify({'status': 'error', 'message': 'Database error'})

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


@app.route('/')
def homepage():
    return render_template('customer/homepage.html')

@app.route('/homepg')
def homepg():
    return render_template('customer/homepg.html')


# LOGIN SIGNUP ROUTES
@app.route('/admin-login')
def admin_login():
    return render_template('admin/admin_login.html')

@app.route('/cust-login')
def cust_login():
    return render_template('customer/cust_login.html')

@app.route('/signup')
def signup():
    return render_template('customer/signup.html')
# LOGIN SIGNUP ROUTES

# SKY CUST ROUTES
@app.route('/profile')
def profile():
    return render_template('customer/profile.html')

@app.route('/message')
def messages():
    return render_template('customer/messages.html')

@app.route('/chat')
def chat():
    return render_template('customer/chat.html')

@app.route('/favourites')
def favourites():
    return render_template('customer/favourites.html')

@app.route('/points')
def points():
    return render_template('customer/points_shop.html')

@app.route('/vouchers')
def vouchers():
    return render_template('customer/vouchers.html')
# SKY CUST ROUTES

#SKY ADMIN ROUTES
@app.route('/admin-profile')
def admin_profile():
    return render_template('admin/admin_profile.html')

@app.route('/user-management')
def user_management():
    return render_template('admin/user_management.html')

@app.route('/user-profile')
def user_profile():
    return render_template('admin/user_profile.html')
#SKY ADMIN ROUTES

@app.route('/Blog')
def blog():
    return render_template('customer/blogpost.html')

@app.route('/createpost', methods=['GET', 'POST'])
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
        return redirect(url_for('MyPosts'))
    return render_template("customer/createpost.html", form=form)

@app.route('/myposts')
def MyPosts():
    return render_template('customer/myposts.html', Posts = Posts)

@app.route('/myposts/<int:id>/')
def ViewPost(id):
    post = next((post for post in Posts if post['id'] == id), None)
    if post is None:
        abort(404)  # Return a 404 error if the post is not found
    return render_template('customer/viewpost.html', post=post)


# remember to set to False when done with project
if __name__ == "__main__":
    app.run(debug=True)