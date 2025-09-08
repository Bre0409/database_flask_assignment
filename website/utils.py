from functools import wraps
from flask import session, redirect, url_for, flash

def login_required_db(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "user_id" not in session:
            flash("Please log in first.", category="warning")
            return redirect(url_for("auth.login"))
        return f(*args, **kwargs)
    return decorated_function
