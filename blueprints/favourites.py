from flask import Blueprint, render_template, session, redirect, url_for, request, flash
from db import get_db_connection
from blueprints.sky_forms import AddFavouritesForm, SearchbarForm
from blueprints.utils import *
import base64

fav_bp = Blueprint('fav', __name__)

def insert_into_fav(user_id: int, post_id: int):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("INSERT INTO user_favourites (user_id, post_id) VALUES  (%s, %s)", (user_id, post_id))
    conn.commit()
    cursor.close()
    conn.close()

def remove_from_fav(user_id: int, post_id: int):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("DELETE FROM user_favourites WHERE user_id = %s AND post_id = %s", (user_id, post_id))
    conn.commit()
    cursor.close()
    conn.close()

def get_fav(user_id: int):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT uf.user_id, uf.post_id, p.header, p.body, p.image_data
        FROM user_favourites uf
        INNER JOIN posts p ON uf.post_id = p.post_id
        WHERE uf.user_id = %s
        ORDER BY favourite_id desc;
    """, (user_id,))
    favourites = cursor.fetchall()

    for favourite in favourites:
        if favourite['image_data']:
            favourite['image_data'] = base64.b64encode(favourite['image_data']).decode('utf-8')

    cursor.close()
    conn.close()
    return favourites

@fav_bp.route('/favourites')
@user_required
def favourites():
    searchbar_form = SearchbarForm()
    add_favourites_form = AddFavouritesForm()
    favourites = get_fav(session['_user_id'])
    return render_template('user/favourites.html', favourites=favourites, add_favourites_form=add_favourites_form, searchbar_form=searchbar_form)

@fav_bp.route('/add_favourite', methods=['POST'])
@user_required
def add_favourite():
    form = AddFavouritesForm()
    if form.validate_on_submit():
        user_id = session.get('_user_id')
        post_id = request.form.get('post_id')

        if user_id and post_id:
            insert_into_fav(user_id, int(post_id))
            return redirect(url_for('bp.post', post_id=post_id))

    return redirect(url_for('fav.favourites'))

@fav_bp.route('/remove_favourite', methods=['POST'])
@user_required
def remove_favourite():
    form = AddFavouritesForm()
    if form.validate_on_submit():
        user_id = session.get('_user_id')
        post_id = request.form.get('post_id')

        if user_id and post_id:
            remove_from_fav(user_id, int(post_id))
            return redirect(url_for('bp.post', post_id=post_id))

    return redirect(url_for('fav.favourites'))
