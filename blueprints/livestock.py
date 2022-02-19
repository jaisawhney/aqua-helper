from flask import Blueprint, render_template
from flask_login import login_user, logout_user

from forms import AquariumLivestockForm
from models import Livestock
from db import db

livestock_views = Blueprint("livestock", __name__, url_prefix="/livestock")


@livestock_views.route("/")
def index():
    return "Livestock index"
