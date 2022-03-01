from unittest import TestCase
from werkzeug.security import generate_password_hash
from models import User, Aquarium, Livestock
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


def create_livestock():
    livestock = Livestock(aquarium_id=1, name="Clownfish", quantity=2,
                          added_on=date.today())
    db.session.add(livestock)
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
        create_livestock()

        self.app.post("/login", data={"email": "john.doe@example.com", "password": "mypassword"})

        res = self.app.get("/aquariums/1/livestock/")
        self.assertEqual(res.status_code, 200)

        res_text = res.get_data(as_text=True)
        self.assertIn("Livestock for", res_text)
        self.assertIn("Clownfish", res_text)

    def test_create(self):
        create_user()
        create_aquarium()

        self.app.post("/login", data={"email": "john.doe@example.com", "password": "mypassword"})
        self.app.post("/aquariums/1/livestock/new/",
                      data={"name": "Shrimp", "quantity": 1, "added_on": date.today()})

        res = self.app.get("/aquariums/1/livestock/")
        self.assertEqual(res.status_code, 200)

        res_text = res.get_data(as_text=True)
        self.assertIn("Livestock for", res_text)
        self.assertIn("Shrimp", res_text)
