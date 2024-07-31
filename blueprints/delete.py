from flask import Blueprint, redirect, url_for, flash
from flask_login import login_required
from flask_wtf.csrf import CSRFError

from db import get_db_connection

delete_bp = Blueprint('delete', __name__)


@delete_bp.route('/deletepost/<int:post_id>', methods=['POST'])
@login_required
def delete_post(post_id):
    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("DELETE FROM posts WHERE post_id = %s", (post_id,))
        conn.commit()
        print("deleted")
        flash("Post deleted successfully!", "success")
    except Exception as e:
        conn.rollback()
        flash("An error occurred while deleting the post.", "error")
    finally:
        cursor.close()
        conn.close()

    return redirect(url_for('myposts.my_posts'))

@delete_bp.errorhandler(CSRFError)
def handle_csrf_error(e):
    flash(f'CSRF Error: {e.description}', 'error')
    return redirect(url_for('myposts.my_posts'))
