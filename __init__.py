import os

from flask import Flask, request, jsonify, render_template, flash, url_for, redirect, abort
from werkzeug.utils import secure_filename
from wtforms.fields import datetime

from chat import get_response

from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField, FileField, SelectField
from datetime import datetime
from wtforms.validators import DataRequired, Length
from flask_wtf.file import FileAllowed

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

#
# @app.route('/')
# def home():
#     return "Hello, Flask!"


# chatbot
@app.post("/predict")
def predict():
    text = request.get_json().get("message")
    response = get_response(text)
    message = {"answer": response}
    return jsonify(message)


@app.route('/')
def homepage():
    return render_template('customer/homepage.html')

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
@app.route('/user-management')
def user_management():
    return render_template('admin/user_management.html')
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