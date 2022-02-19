from flask import Blueprint, render_template
from flask_login import login_user, logout_user

from forms import AquariumActionsForm
from models import Action
from db import db

actions_views = Blueprint("actions", __name__, url_prefix="/actions")


@actions_views.route("/")
def index():
    return "Actions index"
