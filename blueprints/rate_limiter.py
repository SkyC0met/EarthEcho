import time
from functools import wraps
from flask import request, session, flash, redirect, url_for

rate_limit_store = {}

def rate_limit(max_per_minute):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            user_id = session['_user_id']
            if request.method == 'POST':
                receiver = request.form.get('receiver')
                if not user_id:
                    return redirect(url_for('auth.cust_login'))

                current_time = time.time()
                if user_id in rate_limit_store:
                    timestamps, count = rate_limit_store[user_id]
                    rate_limit_store[user_id][0] = [ts for ts in timestamps if current_time - ts < 60]
                    rate_limit_store[user_id][1] = len(rate_limit_store[user_id][0])

                    if count >= max_per_minute:
                        flash('Rate limit exceeded. Please wait a moment before sending more messages.', 'warning')
                        return redirect(url_for('messaging.messages'))
                
            return f(*args, **kwargs)
        return decorated_function
    return decorator
