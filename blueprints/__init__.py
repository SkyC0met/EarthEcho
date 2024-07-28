import os
from flask import Blueprint, request, jsonify, render_template, flash, url_for, redirect, abort
from werkzeug.utils import secure_filename
from datetime import datetime
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField, SelectField
from wtforms.validators import DataRequired, Length
from flask_wtf.file import FileField, FileAllowed
from blueprints.chatbot.chat import get_response

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
    title = StringField('Title', validators=[DataRequired(), Length(min=1, max=100)])
    text = TextAreaField('Text', validators=[DataRequired()])
    topic = SelectField('Topic', choices=[('Sustainability', "Sustainability"), ('Electricity', "Electricity"), ('Pollution', 'Pollution'), ('recycling', 'recycling')])
    image = FileField('Image', validators=[DataRequired(), FileAllowed(['jpg', 'png'])])
    submit = SubmitField('Post!')

# chatbot
@init_bp.post("/predict")
def predict():
    text = request.get_json().get("message")
    response = get_response(text)
    message = {"answer": response}
    return jsonify(message)

@init_bp.route('/')
def homepage():
    return render_template('customer/homepage.html')

# SKY CUST ROUTES
@init_bp.route('/profile')
def profile():
    return render_template('customer/profile.html')

@init_bp.route('/favourites')
def favourites():
    return render_template('customer/favourites.html')

@init_bp.route('/vouchers')
def vouchers():
    return render_template('customer/vouchers.html')

# SKY ADMIN ROUTES
@init_bp.route('/admin-profile')
def admin_profile():
    return render_template('admin/admin_profile.html')

@init_bp.route('/user-management')
def user_management():
    return render_template('admin/user_management.html')

@init_bp.route('/user-profile')
def user_profile():
    return render_template('admin/user_profile.html')

@init_bp.route('/points')
def points():
    return render_template('customer/points_shop.html')

# Blog
@init_bp.route('/Blog')
def blog():
    return render_template('customer/blogpost.html')

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
    return render_template("customer/createpost.html", form=form)

@init_bp.route('/myposts')
def MyPosts():
    return render_template('customer/myposts.html', Posts=Posts)

@init_bp.route('/myposts/<int:id>/')
def ViewPost(id):
    post = next((post for post in Posts if post['id'] == id), None)
    if post is None:
        abort(404)  # Return a 404 error if the post is not found
    return render_template('customer/viewpost.html', post=post)
