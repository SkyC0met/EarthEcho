from flask import Flask
from config import Config

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    app.secret_key = app.config['SECRET_KEY']

    from blueprints.auth import auth_bp
    from blueprints.__init__ import init_bp
    from blueprints.messaging import messaging_bp
    from blueprints.misc import misc_bp
    from blueprints.review import review_bp
    from blueprints.unban import unban_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(init_bp)
    app.register_blueprint(messaging_bp)
    app.register_blueprint(misc_bp)
    app.register_blueprint(review_bp)
    app.register_blueprint(unban_bp)

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, host='127.0.0.1', port=80)
