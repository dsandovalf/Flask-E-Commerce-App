from flask_httpauth import HTTPBasicAuth, HTTPTokenAuth
from app.models import User
from flask import g


basic_auth = HTTPBasicAuth()
token_auth = HTTPTokenAuth()

@basic_auth.verify_password
def verify_password(email, password):
    # check if user exists
    u = User.query.filter_by(email=email).first()
    if u is None:
        return False
    g.current_user = u
    # check password
    return u.check_hashed_password(password)

@token_auth.verify_token
def verify_token(token):
    u = User.check_token(token) if token else None
    g.current_user = u
    return g.current_user or None