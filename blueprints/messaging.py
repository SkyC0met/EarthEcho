from flask import Blueprint, render_template, request, jsonify, session, redirect, url_for
from db import get_db_connection
from blueprints.utils import login_required
from blueprints.sky_forms import MessageForm

messaging_bp = Blueprint('messaging', __name__)

def get_all_users(exclude_user_id: int):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM users WHERE user_id != %s", (exclude_user_id,))
    users = cursor.fetchall()
    cursor.close()
    conn.close()
    return users

@messaging_bp.route('/messages')
@login_required
def messages():
    return render_template('customer/messages.html')

@messaging_bp.route('/all-users')
@login_required
def all_users():
    users = get_all_users(session['user_id'])
    return render_template('customer/all_users.html', users=users)

@messaging_bp.route('/chat/<receiver>')
@login_required
def chat(receiver):
    form = MessageForm()
    if form.validate_on_submit():
            return render_template('customer/chat.html', receiver=receiver, form=form)
    return render_template('customer/chat.html', receiver=receiver, form=form)

def insert_message(sender_user_id: int, sender: str, receiver: str, message: str):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO messages (sender_user_id, sender, receiver, message) VALUES (%s, %s, %s, %s)",
        (sender_user_id, sender, receiver, message)
    )
    conn.commit()
    cursor.close()
    conn.close()

@messaging_bp.route('/send_message', methods=['POST'])
@login_required
def send_message():
    sender = session['name']
    receiver = request.form['receiver']
    message = request.form['message']
    insert_message(session['user_id'], sender, receiver, message)
    return jsonify({'status': 'Message sent successfully!'})


"""

def get_messages_between_users(sender: str, receiver: str):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute(
        "SELECT * FROM messages WHERE (sender = %s AND receiver = %s) OR (sender = %s AND receiver = %s) ORDER BY timestamp",
        (sender, receiver, receiver, sender)
    )
    messages = cursor.fetchall()
    cursor.close()
    conn.close()
    return messages

def clear_all_messages():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM messages")
    cursor.execute("ALTER TABLE messages AUTO_INCREMENT = 1")
    conn.commit()
    cursor.close()
    conn.close()"""

"""@messages_bp.route('/home')
def home():
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))
    users = get_all_users(session['user_id'])
    return render_template('home.html', users=users)

@messages_bp.route('/send_message', methods=['POST'])
def send_message():
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))
    sender = session['name']
    receiver = request.form['receiver']
    message = request.form['message']
    insert_message(session['user_id'], sender, receiver, message)
    return jsonify({'status': 'Message sent successfully!'})

@messages_bp.route('/get_messages', methods=['GET'])
def get_messages():
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))
    sender = session['name']
    receiver = request.args.get('receiver')
    messages = get_messages_between_users(sender, receiver)
    return jsonify(messages)

@messages_bp.route('/clear_messages', methods=['POST'])
def clear_messages():
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))
    clear_all_messages()
    return redirect(url_for('messaging.home'))

@messages_bp.route('/message/<receiver>')
def message_page(receiver):
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))
    return render_template('message.html', receiver=receiver)
"""