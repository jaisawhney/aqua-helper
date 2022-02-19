from flask import Blueprint, render_template
from flask_login import login_user, logout_user

from forms import AquariumForm
from models import Aquarium
from db import db

aquariums_views = Blueprint("aquariums", __name__, url_prefix="/aquariums")


@aquariums_views.route("/")
def index():
    return "Aquariums index"
