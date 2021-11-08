from flask import Blueprint

bp = Blueprint('shop', __name__, url_prefix='')

from .import routes, models