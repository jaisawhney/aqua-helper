from unittest import TestCase
from werkzeug.security import generate_password_hash
from models import User, Aquarium
from db import db
from app import app


def create_user():
    user = User(email="john.doe@example.com", password=generate_password_hash("mypassword"))
    db.session.add(user)
    db.session.commit()


def create_aquarium():
    aquarium = Aquarium(user_id=1, name="My Aquarium")
    db.session.add(aquarium)
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

        self.app.post("/login", data={"email": "john.doe@example.com", "password": "mypassword"})

        res = self.app.get("/aquariums/")
        self.assertEqual(res.status_code, 200)

        res_text = res.get_data(as_text=True)
        self.assertIn("Aquariums", res_text)
        self.assertIn("Create New", res_text)
        self.assertIn("My Aquarium", res_text)

    def test_create(self):
        create_user()

        self.app.post("/login", data={"email": "john.doe@example.com", "password": "mypassword"})
        self.app.post("/aquariums/new/", data={"name": "Cube Aquarium"})

        res = self.app.get("/aquariums/")
        self.assertEqual(res.status_code, 200)

        res_text = res.get_data(as_text=True)
        self.assertIn("Aquariums", res_text)
        self.assertIn("Create New", res_text)
        self.assertIn("Cube Aquarium", res_text)

    def test_update(self):
        create_user()
        create_aquarium()

        self.app.post("/login", data={"email": "john.doe@example.com", "password": "mypassword"})
        self.app.post("/aquariums/1/edit/", data={"name": "Renamed Aquarium"})

        res = self.app.get("/aquariums/")
        self.assertEqual(res.status_code, 200)

        res_text = res.get_data(as_text=True)
        self.assertIn("Aquariums", res_text)
        self.assertIn("Create New", res_text)
        self.assertIn("Renamed Aquarium", res_text)
