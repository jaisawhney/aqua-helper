from flask import Blueprint

main_views = Blueprint("main", __name__)


@main_views.route("/")
def index():
    return "Hello world!"
