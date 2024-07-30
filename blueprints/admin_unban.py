from flask import Blueprint, render_template, request, redirect, url_for, flash
import mysql.connector
from flask_login import login_required
from db import get_db_connection

# Initialize Blueprint
admin_unban_bp = Blueprint('admin_unban', __name__)

@admin_unban_bp.route('/unban_requests', methods=['GET'])
@login_required
def unban_requests():
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    cursor.execute('SELECT * FROM unban_requests ORDER BY created_at DESC')
    requests = cursor.fetchall()
    cursor.close()
    connection.close()

    return render_template('admin_unban_request.html', requests=requests)

@admin_unban_bp.route('/unban/<int:request_id>', methods=['POST'])
@login_required
def unban(request_id):
    connection = get_db_connection()
    cursor = connection.cursor()
    try:
        cursor.execute('DELETE FROM unban_requests WHERE id = %s', (request_id,))
        connection.commit()
        flash('User has been unbanned successfully.', 'success')
    except mysql.connector.Error as err:
        flash(f'Error: {err}', 'error')
    finally:
        cursor.close()
        connection.close()

    return redirect(url_for('admin.unban_requests'))

@admin_unban_bp.route('/delete/<int:request_id>', methods=['POST'])
@login_required
def delete_request(request_id):
    connection = get_db_connection()
    cursor = connection.cursor()
    try:
        cursor.execute('DELETE FROM unban_requests WHERE id = %s', (request_id,))
        connection.commit()
        flash('Unban request has been deleted.', 'success')
    except mysql.connector.Error as err:
        flash(f'Error: {err}', 'error')
    finally:
        cursor.close()
        connection.close()

    return redirect(url_for('admin.unban_requests'))
