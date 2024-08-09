from flask import Flask, session, send_from_directory, request
from config import Config
from flask_wtf.csrf import CSRFProtect, CSRFError
from flask import jsonify
from datetime import timedelta
from blueprints.utils import login_manager
from flask_talisman import Talisman
from authlib.integrations.flask_client import OAuth

# BLUEPRINTS
from blueprints.__init__ import init_bp
from blueprints.homepage import homepage_bp
from blueprints.admin import admin_bp
from blueprints.auth import auth_bp
from blueprints.profile import profile_bp
from blueprints.messaging import messaging_bp
from blueprints.favourites import fav_bp
from blueprints.reward import reward_bp
from blueprints.misc import misc_bp
from blueprints.review import review_bp
from blueprints.unban import unban_bp
from blueprints.admin_unban import admin_unban_bp
from blueprints.createpost import create_bp
from blueprints.myposts import myposts_bp
from blueprints.viewpost import view_bp
from blueprints.edit import edit_bp
from blueprints.blogpost import blogpost_bp

csp = {
    'default-src': ['\'self\'', '*'],
    'script-src': ['\'self\'', '*', '\'unsafe-inline\'', '\'unsafe-eval\''],
    'style-src': ['\'self\'', '*', '\'unsafe-inline\''],
    'img-src': ['\'self\'', 'data:', '*'],
    'font-src': ['\'self\'', '*'],
    'connect-src': ['\'self\'', '*'],
    'object-src': ['*'],
    'frame-ancestors': ['*']
}

hsts = {
    'max_age': 31536000,
    'include_subdomains': True,
    'preload': True
}

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    app.secret_key = app.config['SECRET_KEY']

    app.config['UPLOAD_FOLDER'] = 'static/images/user_post_images'

    # Initialize OAuth
    oauth = OAuth(app)
    app.extensions['authlib'] = {'oauth': oauth}

    google = oauth.register(
        name='google',
        client_id=app.config['GOOGLE_CLIENT_ID'],
        client_secret=app.config['GOOGLE_CLIENT_SECRET'],
        authorize_url='https://accounts.google.com/o/oauth2/auth',
        access_token_url='https://accounts.google.com/o/oauth2/token',
        access_token_params=None,
        redirect_uri='http://127.0.0.1:80/user/login/google/authorized',
        api_base_url='https://www.googleapis.com/oauth2/v1/',
        access_token_method='POST',
        userinfo_endpoint='https://www.googleapis.com/oauth2/v2/userinfo',
        jwks_uri='https://www.googleapis.com/oauth2/v3/certs',
        scope='openid profile email',
    )

    csrf = CSRFProtect(app)
    login_manager.init_app(app)
    login_manager.login_view = 'auth.user_login'
    login_manager.login_message_category = "primary"

    talisman = Talisman(
        app,
        content_security_policy=csp,
        force_https=True,
        frame_options='DENY',
        referrer_policy='same-origin',
        strict_transport_security=hsts,
        session_cookie_secure=True,
        session_cookie_samesite='Strict',
        x_content_type_options=True,
        x_xss_protection=True
    )

    # Timeout after 30 mins
    app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=30)
    # Remove remember cookie
    app.config['REMEMBER_COOKIE_DURATION'] = timedelta(days=7)

    app.config['SESSION_COOKIE_SECURE'] = True
    app.config['SESSION_COOKIE_HTTPONLY'] = True
    app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'


    # reCAPTCHA
    app.config['RECAPTCHA_SITE_KEY'] = '6LeDmxsqAAAAAIQKTcChogPkiUnenRppl4WiXGh0'
    app.config['RECAPTCHA_SECRET_KEY'] = '6LeDmxsqAAAAALGcfuu8CLdH92N_SHfM5T1xvGTK'

    # Register your blueprints
    app.register_blueprint(init_bp)
    app.register_blueprint(homepage_bp)
    app.register_blueprint(admin_bp, url_prefix='/admin')
    app.register_blueprint(auth_bp, url_prefix='/user')
    app.register_blueprint(profile_bp)
    app.register_blueprint(messaging_bp)
    app.register_blueprint(fav_bp)
    app.register_blueprint(reward_bp)
    app.register_blueprint(misc_bp)
    app.register_blueprint(review_bp)
    app.register_blueprint(unban_bp)
    app.register_blueprint(admin_unban_bp)
    app.register_blueprint(create_bp)
    app.register_blueprint(myposts_bp)
    app.register_blueprint(view_bp)
    app.register_blueprint(edit_bp)
    app.register_blueprint(blogpost_bp)


    @app.errorhandler(CSRFError)
    def handle_csrf_error(e):
        return jsonify({"error": "CSRF token missing or incorrect."}), 400

    @app.route('/check-session')
    def check_session():
        print(session)
        return 'Check the console for session data'

    # Middleware to set the necessary headers
    @app.after_request
    def add_security_headers(response):
        response.headers['Cross-Origin-Opener-Policy'] = 'same-origin'
        response.headers['Cross-Origin-Embedder-Policy'] = 'require-corp'
        return response

    # Serve the game page
    @app.route('/game/index.html')
    def game():
        return send_from_directory('game', 'index.html')

    # Serve static files (JavaScript, images, etc.)
    @app.route('/game/<path:path>')
    def serve_static_file(path):
        return send_from_directory('game', path)

    # API endpoint to update the coin count
    @app.route('/update_coins', methods=['GET'])
    def update_coins():
        global coin_count
        coin_count = int(request.args.get('coin_count', 0))
        return jsonify({'status': 'success', 'coin_count': coin_count})

    # API endpoint to get the current coin count
    @app.route('/get_coin_count', methods=['GET'])
    def get_coin_count():
        global coin_count
        return jsonify({'coin_count': coin_count})

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, host='127.0.0.1', port=80)


