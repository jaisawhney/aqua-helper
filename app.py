from flask import Flask
from db import db
from blueprints.main import main_views
from flask_login import LoginManager

import models
import os

app = Flask(__name__)
app.config.update(
    SECRET_KEY=os.environ.get("SECRET_KEY", os.urandom(6)),
    SQLALCHEMY_DATABASE_URI=os.getenv("DATABASE_URL", "sqlite:///database.db"),
    SQLALCHEMY_TRACK_MODIFICATIONS=False
)

login_manager = LoginManager(app=app)
login_manager.login_view = "auth.login"


@login_manager.user_loader
def load_user(user_id):
    print("test")
    return models.User.query.get(user_id)


@app.before_first_request
def create_db():
    db.create_all()


app.register_blueprint(main_views)

if __name__ == "__main__":
    db.init_app(app)
    app.run(host="0.0.0.0", port=os.environ.get("PORT", 3000))
