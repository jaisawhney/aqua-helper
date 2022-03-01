from unittest import TestCase
from werkzeug.security import generate_password_hash
from models import User, Aquarium, Action
from db import db
from app import app
from datetime import date


def create_user():
    user = User(email="john.doe@example.com", password=generate_password_hash("mypassword"))
    db.session.add(user)
    db.session.commit()


def create_aquarium():
    create_user()
    aquarium = Aquarium(user_id=1, name="My Aquarium")
    db.session.add(aquarium)
    db.session.commit()


def create_action():
    action = Action(aquarium_id=1, name="Example Action", description="Description",
                      due_on=date.today())
    db.session.add(action)
    db.session.commit()


class AuthTests(TestCase):
    def setUp(self):
        app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"
        app.config["WTF_CSRF_ENABLED"] = False
        self.app = app.test_client()

        db.init_app(app)
        app.app_context().push()
        db.drop_all()
        db.create_all()

    def test_index(self):
        create_user()
        create_aquarium()
        create_action()

        self.app.post("/login", data={"email": "john.doe@example.com", "password": "mypassword"})

        res = self.app.get("/aquariums/1/actions/")
        self.assertEqual(res.status_code, 200)

        res_text = res.get_data(as_text=True)
        self.assertIn("Actions for", res_text)
        self.assertIn("Example Action", res_text)

    def test_create(self):
        create_user()
        create_aquarium()

        self.app.post("/login", data={"email": "john.doe@example.com", "password": "mypassword"})
        self.app.post("/aquariums/1/actions/new/",
                      data={"name": "Clean", "description": "Change water", "due_on": date.today()})

        res = self.app.get("/aquariums/1/actions/")
        self.assertEqual(res.status_code, 200)

        res_text = res.get_data(as_text=True)
        self.assertIn("Actions for", res_text)
        self.assertIn("Clean", res_text)
        self.assertIn("Change water", res_text)

    def test_update(self):
        create_user()
        create_aquarium()
        create_action()

        self.app.post("/login", data={"email": "john.doe@example.com", "password": "mypassword"})
        self.app.post("/aquariums/1/actions/1/edit/",
                      data={"name": "Updated Action", "description": "Description", "due_on": date.today()})

        res = self.app.get("/aquariums/1/actions/")
        self.assertEqual(res.status_code, 200)

        res_text = res.get_data(as_text=True)
        self.assertIn("Actions for", res_text)
        self.assertIn("Updated Action", res_text)
