# rate_limiter.py
import time
from functools import wraps
from flask import request, session, flash, redirect, url_for

rate_limit_store = {}

def rate_limit(max_per_minute):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            user_id = session.get('_user_id')
            if not user_id:
                return redirect(url_for('auth.cust_login'))

            if request.method == 'POST':
                current_time = time.time()
                timestamps = rate_limit_store.get(user_id, [])

                # Filter out timestamps older than 60 seconds
                timestamps = [ts for ts in timestamps if current_time - ts < 60]

                # Update the rate limit store with filtered timestamps
                rate_limit_store[user_id] = timestamps

                # Check if the user has exceeded the rate limit
                if len(timestamps) >= max_per_minute:
                    flash('Rate limit exceeded. Please wait a moment before sending more messages.', 'warning')
                    return redirect(url_for('messaging.messages'))

                # Add current time to the timestamps
                timestamps.append(current_time)
                rate_limit_store[user_id] = timestamps

            return f(*args, **kwargs)
        return decorated_function
    return decorator
