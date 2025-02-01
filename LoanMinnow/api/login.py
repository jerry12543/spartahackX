"""Authentication tools for the API."""
from functools import wraps
import flask
import loanminnow
import hashlib

def requires_auth(f):
    """Authenticate  the user."""
    @wraps(f)
    def auth(*args, **kwargs):
        """Authenticate using the session or HTTP Basic Auth."""
        auth = flask.request.authorization
        if not auth or not check_auth(auth['username'], auth['password']):
            return session_auth(*args, **kwargs)
        return f(*args, **kwargs)

    def session_auth(*args, **kwargs):
        """Authenticate using the session."""
        if 'logname' not in flask.session:
            return flask.abort(403)
        return f(*args, **kwargs)
    return auth

def compute_hash_db_string(algorithm, salt, pword):
    """Compute the hash of a password and return the hash in the format."""
    hash_obj = hashlib.new(algorithm)
    password_salted = salt + pword
    hash_obj.update(password_salted.encode('utf-8'))
    password_hash = hash_obj.hexdigest()
    password_db_string = "$".join([algorithm, salt, password_hash])
    return password_db_string


def check_auth(username, pword):
    """Check if the username and password are valid."""
    if not username or not pword:
        return False
    connection = loanminnow.model.get_db()
    cur = connection.execute(
        "SELECT u.password FROM users as u WHERE username = ?",
        (username,)
    )
    user = cur.fetchone()
    if not user:
        return False
    password_db_string = user["password"]
    algorithm, salt, password_hash = password_db_string.split("$")

    password_to_check = compute_hash_db_string(algorithm, salt, pword)
    _, _, computed_hash = password_to_check.split("$")

    return computed_hash == password_hash
