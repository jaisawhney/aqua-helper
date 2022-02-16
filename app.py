from flask import Flask
from db import db
import models
import os

app = Flask(__name__)

app.config.update(
    SECRET_KEY=os.environ.get("SECRET_KEY", os.urandom(6)),
    SQLALCHEMY_DATABASE_URI=os.getenv("DATABASE_URL", "sqlite:///database.db"),
    SQLALCHEMY_TRACK_MODIFICATIONS=False
)


@app.before_first_request
def create_db():
    db.create_all()


@app.route("/")
def index():
    return "Hello World!"


if __name__ == "__main__":
    db.init_app(app)
    app.run(host="0.0.0.0", port=os.environ.get("PORT", 3000))
