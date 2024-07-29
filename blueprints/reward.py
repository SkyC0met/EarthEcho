from flask import Blueprint, render_template, redirect, url_for, flash, session, request
from db import get_db_connection
from blueprints.sky_forms import RedeemVoucherForm, AddPointsForm, SpendVoucherForm
from blueprints.utils import *

reward_bp = Blueprint('reward', __name__)

# REWARD VOUCHER FUNCTIONS
def get_points_shop_rewards():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM points_shop ORDER BY points_type, points_required")
    all_rewards = cursor.fetchall()
    cursor.close()
    conn.close()
    return all_rewards

def get_user_points_balance(user_id: int):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT points_balance FROM user_points WHERE user_id = %s", (user_id,))
    result = cursor.fetchone()
    cursor.close()
    conn.close()
    if result:
        return result['points_balance']
    return 0

def redeem_voucher(user_id: int, reward_id: int):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT points_balance FROM user_points WHERE user_id = %s", (user_id,))
    user_points = cursor.fetchone()
    
    cursor.execute("SELECT points_required FROM points_shop WHERE reward_id = %s", (reward_id,))
    reward = cursor.fetchone()

    if user_points and reward:
        if user_points['points_balance'] >= reward['points_required']:
            cursor.execute("INSERT INTO user_redemption (user_id, reward_id) VALUES (%s, %s)", (user_id, reward_id))
            cursor.execute("UPDATE user_points SET points_balance = points_balance - %s WHERE user_id = %s", (reward['points_required'], user_id))
            conn.commit()
            cursor.close()
            conn.close()
            return True
        else:
            print(f"Insufficient points: {user_points['points_balance']} required: {reward['points_required']}")
    else:
        print(f"Failed to fetch user points or reward details: user_points={user_points}, reward={reward}, reward_id={reward_id}")

    cursor.close()
    conn.close()
    return False

def get_vouchers(user_id: int):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT ur.user_id, ur.reward_id, ur.redemption_date, ps.reward_name, ps.reward, ps.reward_desc, ps.valid_until, ps.image_path
        FROM user_redemption ur
        INNER JOIN points_shop ps ON ur.reward_id = ps.reward_id
        WHERE ur.user_id = %s;
    """, (user_id,))
    vouchers = cursor.fetchall()
    cursor.close()
    conn.close()
    return vouchers

def spend_voucher(user_id: int, reward_id: int):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        DELETE FROM user_redemption 
        WHERE user_id = %s AND reward_id = %s 
        ORDER BY redemption_date LIMIT 1
    """, (user_id, reward_id))
    conn.commit()
    cursor.close()
    conn.close()

# REWARD VOUCHER FUNCTIONS

# REWARD VOUCHER ROUTES
@reward_bp.route('/points-shop', methods=['GET', 'POST'])
@user_required
def points_shop():
    redeem_voucher_form = RedeemVoucherForm()
    add_points_form = AddPointsForm()

    if redeem_voucher_form.validate_on_submit():
        reward_id = redeem_voucher_form.reward_id.data
        print(f"Redeeming voucher with reward_id: {reward_id}")

        if reward_id:
            if redeem_voucher(session['_user_id'], reward_id):
                flash('Voucher redeemed successfully!', 'success')
            else:
                flash("You don't have enough points to redeem this voucher", 'primary')
        else:
            print("reward_id is not present in the form data")
        
        return redirect(url_for('reward.points_shop'))
    
    points_balance = get_user_points_balance(session['_user_id'])
    all_rewards = get_points_shop_rewards()
    food_rewards = [reward for reward in all_rewards if reward['points_type'] == 'food']
    fashion_rewards = [reward for reward in all_rewards if reward['points_type'] == 'fashion']
    return render_template('user/points_shop.html', points_balance=points_balance, food_rewards=food_rewards, fashion_rewards=fashion_rewards, redeem_voucher_form=redeem_voucher_form, add_points_form=add_points_form)

@reward_bp.route('/vouchers', methods=['GET', 'POST'])
@user_required
def vouchers():
    spend_voucher_form = SpendVoucherForm()
    if spend_voucher_form.validate_on_submit():
        voucher_id = request.form.get("voucher")
        if voucher_id:
            spend_voucher(session['_user_id'], voucher_id)
            flash('Voucher spent successfully!', 'success')
        return redirect(url_for('reward.vouchers'))

    vouchers = get_vouchers(session['_user_id'])
    return render_template('user/vouchers.html', vouchers=vouchers, spend_voucher_form=spend_voucher_form)

def add_points_to_user(user_id: int):
    points_to_add = 1000
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT points_balance FROM user_points WHERE user_id = %s", (user_id,))
    result = cursor.fetchone()

    if result:
        cursor.execute("UPDATE user_points SET points_balance = points_balance + %s WHERE user_id = %s", (points_to_add, user_id))
    else:
        cursor.execute("INSERT INTO user_points (user_id, points_balance) VALUES (%s, %s)", (user_id, points_to_add))

    conn.commit()
    cursor.close()
    conn.close()

@reward_bp.route('/add_points', methods=['POST'])
@user_required
def add_points():
    add_points_form = AddPointsForm()
    if add_points_form.validate_on_submit():
        add_points_to_user(session['_user_id'])
        flash('Points added', 'success')
        return redirect(url_for('reward.points_shop'))
    return render_template('user/points_shop.html', add_points_form=add_points_form)

# REWARD VOUCHER ROUTES