from flask import Flask, request, jsonify, render_template, flash, url_for, redirect, abort
from wtforms.fields import datetime

from chat import get_response

from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField, FileField, SelectField
from datetime import datetime
from wtforms.validators import DataRequired
from flask_wtf.file import FileAllowed

app = Flask(__name__)
app.config['SECRET_KEY'] = 'rzstxrdycfuvgibhnj'

image_filename = 'example_image.png'  # replace with the actual filename of your image
image_path = EarthEcho/static/images/electricity.jpg('images', image_filename)
def Posts():
    posts = [
        {
            'id': 1,
            'title': 'How to be sustainable?',
            'text': 'lorem ipsum adhdyj gdh gsshh hu gdh gsh asgasd sdivvvvFVUvjusd cgibsdjhbcu',
            'author': 'John Doe',
            'date_created': '23-01-2024',
            'topic': 'Sustainability'
        },
        {
            'id': 2,
            'title': 'Littering and its effects.',
            'text': 'lorem ipsum adhdyj gdh gsshh hu gdh gsh asgasd sdivvvvFVUvjusd cgibsdjhbcu',
            'author': 'John Doe',
            'date_created': '25-01-2024',
            'topic': 'Pollution'

        },
        {
            'id': 3,
            'title': 'Conserving Energy!',
            'text': 'lorem ipsum adhdyj gdh gsshh hu gdh gsh asgasd sdivvvvFVUvjusd cgibsdjhbcu',
            'author': 'John Doe',
            'date_created': '26-01-2024',
            'topic': 'Electricity',
            'image':
        }
    ]
    return posts

Posts = Posts()

class PostForm(FlaskForm):
    author = "John Doe"
    title = StringField('Title', DataRequired())
    text = TextAreaField('Text', DataRequired())
    topic = SelectField('Topic', choices=[('1', "Sustainability"), ('2', "Electricity"),('3','Pollution'), ('4', 'recycling')])
    image = FileField('Image', validators=[FileAllowed(['jpeg', 'png'])])
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


@app.route('/Blog')
def blog():
    return render_template('customer/blogpost.html')

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

@app.route('/createpost', methods=['GET', 'POST'])
def CreatePosts():
    form = PostForm()
    if form.validate_on_submit():
        author = "John Doe"
        title = form.title.data
        text = form.text.data
        topic = form.topic.data
        flash("Post created!", "success")
        new_post = {
            'id': len(Posts) + 1,
            'title': title,
            'text': text,
            'author': author,
            'date_created': datetime.now().strftime('%d-%m-%Y'),
            'topic': topic
        }
        Posts.append(new_post)
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