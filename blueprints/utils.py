from functools import wraps
from flask import session, redirect, url_for, flash
from db import get_db_connection
# import jwt

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('Please log in to access this page.', 'danger')
            return redirect(url_for('auth.cust_login'))
        return f(*args, **kwargs)
    return decorated_function

def get_user_by_field(field_name: str, field_value):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    query = f"SELECT * FROM users WHERE {field_name} = %s"
    cursor.execute(query, (field_value,))
    user = cursor.fetchone()
    cursor.close()
    conn.close()
    return user

"""def isAuthenticated(f):
    @wraps(f)
    def decorator(*args, **kwargs):
        try:
            token = session.get('token')
            # Decode the token 
            decoded_token = jwt.decode(jwt=token, key='@pp_D3v3l0pMent', algorithms=['HS256'])
        except AttributeError:
            flash('Your session is invalid. Please login.')
            session.clear()
            return redirect(url_for('auth.cust_login'))
        except jwt.ExpiredSignatureError:
            session.clear()
            flash('Your session has expired. Please login.')
            return redirect(url_for('auth.cust_login'))
        except jwt.InvalidTokenError:
            session.clear()
            flash('Your session is invalid. Please login.')
            return redirect(url_for('auth.cust_login'))
        except:
            session.clear()
            flash('Your session is invalid. Please login.')
            return redirect(url_for('auth.cust_login'))
        return f(*args, **kwargs)
    return decorator"""

"""def access_required(roles):
    def wrapper(fn):
        @wraps(fn)
        def decorated_view(*args, **kwargs):
            try:
                acc_type = session.get("acc_type")
            except:
                flash('Your session is invalid. Please login.')
                return redirect(url_for('auth.login'))
            if acc_type == None or acc_type not in roles:
                flash("Unauthorised access.")
                return redirect(url_for('acc.user_home'))
            return fn(*args, **kwargs)
        return decorated_view
    return wrapper"""