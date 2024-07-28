from flask import Blueprint, render_template, session, redirect, url_for
from db import get_db_connection
from blueprints.sky_forms import AddFavouritesForm

fav_bp = Blueprint('fav', __name__)

def insert_into_fav(user_id: int, post_id: int):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("INSERT INTO user_favourites (user_id, post_id) VALUES  (%s, %s)", (user_id, post_id))
    cursor.close()
    conn.close()

def get_fav(user_id: int):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT uf.user_id, uf.post_id, sp.header, sp.body, sp.image_path
        FROM user_favourites uf
        INNER JOIN sky_posts_to_test_fav sp ON uf.post_id = sp.post_id
        WHERE uf.user_id = %s;
    """, (user_id,))
    favourites = cursor.fetchall()
    cursor.close()
    conn.close()
    return favourites

@fav_bp.route('/favourites')
def favourites():
    add_favourites_form = AddFavouritesForm()
    if add_favourites_form.validate_on_submit():
        insert_into_fav(session['_user_id'], 1)
        return redirect(url_for('fav.favourites'))
    
    favourites = get_fav(session['_user_id'])
    return render_template('user/favourites.html', favourites=favourites, add_favourites_form=add_favourites_form)
