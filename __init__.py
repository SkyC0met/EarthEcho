from flask import Flask, request, jsonify, render_template

from chat import get_response

app = Flask(__name__)

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


# remember to set to False when done with project
if __name__ == "__main__":
    app.run(debug=True)