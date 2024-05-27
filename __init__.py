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


@app.route('/points')
def points():
    return render_template('customer/points_shop.html')


# remember to set to False when done with project
if __name__ == "__main__":
    app.run(debug=True)