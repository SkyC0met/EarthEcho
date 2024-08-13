from flask import Blueprint, send_from_directory, jsonify, session, request
from blueprints.utils import *
from blueprints.rate_limiter import *
import mysql

game_bp = Blueprint('game', __name__)

# Serve the game page
@game_bp.route('/game/index.html')
def game():
    return send_from_directory('game', 'index.html')

# Serve static files (JavaScript, images, etc.)
@game_bp.route('/game/<path:path>')
def serve_static_file(path):
    return send_from_directory('game', path)

@game_bp.route('/update_coins', methods=['GET'])
def update_coins():
    global coin_count
    coin_count = int(request.args.get('coin_count', 0))
    update_user_points(session['_user_id'], 1)
    return jsonify({'status': 'success', 'coin_count': coin_count})

@game_bp.route('/get_coin_count', methods=['GET'])
def get_coin_count():
    global coin_count
    return jsonify({'coin_count': coin_count})

@game_bp.route('/update_user_points', methods=['POST'])
def update_user_points(user_id, points):
    if user_id is None or points is None:
        return jsonify({'status': 'error', 'message': 'Missing user_id or points'}), 400

    try:
        connection = get_db_connection()
        cursor = connection.cursor()
        cursor.execute("INSERT INTO user_points (user_id, points_balance) VALUES (%s, %s) ON DUPLICATE KEY UPDATE points_balance = points_balance + %s", (user_id, points, points))
        connection.commit()
        cursor.close()
        connection.close()
        return jsonify({'status': 'success'})
    except mysql.connector.Error as err:
        return jsonify({'status': 'error', 'message': str(err)}), 500