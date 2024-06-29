from flask import session,redirect,url_for
from functools import wraps

def authentication(f):
    @wraps(f)
    def authFunc(*args, **kwargs):
        if 'activeUserData' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return authFunc