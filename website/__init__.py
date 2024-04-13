from flask import Flask


def create_app():
    """
    Fukncja tworząca aplikacje hosta
    """
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'siema'
    return app

