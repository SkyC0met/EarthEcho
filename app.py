from flask import Flask, session, render_template
from config import Config
from flask_wtf.csrf import CSRFProtect, CSRFError
from flask import jsonify
from datetime import timedelta

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    app.secret_key = app.config['SECRET_KEY']
    # timeout after 30 mins
    # app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=30)

    # app.config['SESSION_COOKIE_SECURE'] = True
    # app.config['SESSION_COOKIE_HTTPONLY'] = True
    # app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'

    csrf = CSRFProtect(app)

    from blueprints.auth import auth_bp
    from blueprints.__init__ import init_bp
    from blueprints.messaging import messaging_bp
    from blueprints.misc import misc_bp
    from blueprints.review import review_bp
    from blueprints.homepage import homepage_bp
    from blueprints.profile import profile_bp
    from blueprints.admin import admin_bp
    from blueprints.reward import reward_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(init_bp)
    app.register_blueprint(messaging_bp)
    app.register_blueprint(misc_bp)
    app.register_blueprint(review_bp)
    app.register_blueprint(homepage_bp)
    app.register_blueprint(profile_bp)
    app.register_blueprint(admin_bp)
    app.register_blueprint(reward_bp)

    # for chatbot to run
    # csrf.exempt(init_bp)

    @app.errorhandler(CSRFError)
    def handle_csrf_error(e):
        return jsonify({"error": "CSRF token missing or incorrect."}), 400
    
    @app.route('/check-session')
    def check_session():
    # Log the session data
        print(session)
        return 'Check the console for session data'

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, host='127.0.0.1', port=80)
    #app.run(debug=False) to activate 500 error
