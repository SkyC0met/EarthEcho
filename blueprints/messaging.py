from flask import Blueprint, render_template, redirect, url_for, flash, session
from flask_login import login_required
from db import get_db_connection
from blueprints.utils import *
from blueprints.sky_forms import MessageForm

messaging_bp = Blueprint('messaging', __name__)

# MESSAGING FUNCTIONS
def get_users_with_messages(user_id: int):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT DISTINCT 
            CASE
                WHEN sender_user_id = %s THEN receiver_user_id
                ELSE sender_user_id
            END AS user_id
        FROM messages
        WHERE sender_user_id = %s OR receiver_user_id = %s
        """, (user_id, user_id, user_id))
    users = cursor.fetchall()
    cursor.close()
    conn.close()
    return users

def get_last_message_between_users(user_id1: int, user_id2: int):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT message, timestamp 
        FROM messages 
        WHERE (sender_user_id = %s AND receiver_user_id = %s) OR (sender_user_id = %s AND receiver_user_id = %s) 
        ORDER BY timestamp DESC 
        LIMIT 1
    """, (user_id1, user_id2, user_id2, user_id1))
    last_message = cursor.fetchone()
    cursor.close()
    conn.close()
    return last_message

def insert_message(sender_user_id: int, receiver_user_id: int, message: str):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO messages (sender_user_id, receiver_user_id, message) VALUES (%s, %s, %s)",
        (sender_user_id, receiver_user_id, message)
    )
    conn.commit()
    cursor.close()
    conn.close()

def get_messages_between_users(user_id1: int, user_id2: int):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute(
        "SELECT * FROM messages WHERE (sender_user_id = %s AND receiver_user_id = %s) OR (sender_user_id = %s AND receiver_user_id = %s) ORDER BY timestamp",
        (user_id1, user_id2, user_id2, user_id1)
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
    conn.close()

# MESSAGING FUNCTIONS

# MESSAGING ROUTES
@messaging_bp.route('/messages')
@user_required
def messages():
    user_id = session['_user_id']
    users = get_users_with_messages(user_id)
    users_with_last_messages = []
    for user in users:
        last_message = get_last_message_between_users(user_id, user['user_id'])
        user_info = get_user_by_field('user_id', user['user_id'])
        users_with_last_messages.append({
            'user_id': user['user_id'],
            'username': user_info['username'],
            'last_message': last_message['message'],
            'timestamp': last_message['timestamp']
        })
    return render_template('user/messages.html', users=users_with_last_messages)

@messaging_bp.route('/chat/<receiver_id>', methods=['GET', 'POST'])
@user_required
def chat(receiver_id):
    sender_id = session['_user_id']
    if sender_id == int(receiver_id):
        flash('You cannot message yourself.', 'warning')
        return redirect(url_for('messaging.messages'))

    receiver = get_user_by_field('user_id', receiver_id)
    sender = get_user_by_field('user_id', sender_id)
    if not receiver:
        flash('User does not exist.', 'warning')
        return redirect(url_for('messaging.messages'))
        
    message_form = MessageForm()
    message_form.receiver.data = receiver_id
    if message_form.validate_on_submit():
        message = message_form.message.data
        insert_message(sender_id, receiver_id, message)
        return redirect(url_for('messaging.chat', receiver_id=receiver_id))
    messages = get_messages_between_users(sender_id, receiver_id)
    return render_template('user/chat.html', sender=sender['username'], receiver=receiver['username'], message_form=message_form, messages=messages)

@messaging_bp.route('/clear_messages', methods=['POST'])
@user_required
def clear_messages():
    if 'user_id' not in session:
        return redirect(url_for('auth.user_login'))
    clear_all_messages()
    return redirect(url_for('messaging.messages'))

# MESSAGING ROUTES