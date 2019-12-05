from flask import Blueprint

git = Blueprint("gitpull", __name__)

from . import views