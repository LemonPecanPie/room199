# this file was made by lord lemon pecan pie
# why won't flask work ;((((((((

import flask

app = flask.Flask(__name__)


@app.route('/')
def hello_world():
    return "<p>Hello, World!</p>"
