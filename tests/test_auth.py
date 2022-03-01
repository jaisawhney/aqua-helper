from unittest import TestCase
from werkzeug.security import generate_password_hash
from models import User
from db import db
from app import app


def create_user():
    user = User(email="john.doe@example.com", password=generate_password_hash("mypassword"))
    db.session.add(user)
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

    def test_register(self):
        self.app.post("/register", data={"email": "john.doe@example.com", "password": "Abcdefg"})

        created_user = User.query.filter_by(email="john.doe@example.com").first()
        self.assertIsNotNone(created_user)

    def test_register_existing(self):
        create_user()

        res = self.app.post("/register", data={"email": "john.doe@example.com", "password": "mypassword"})

        res_text = res.get_data(as_text=True)
        self.assertIn("That email is already being used!", res_text)

    def test_login(self):
        create_user()

        self.app.post("/login", data={"email": "john.doe@example.com", "password": "mypassword"})

        res = self.app.get("/", follow_redirects=True)
        self.assertEqual(res.status_code, 200)

        res_text = res.get_data(as_text=True)
        self.assertIn("Logout", res_text)

    def test_login_incorrect_email(self):
        create_user()

        res = self.app.post("/login", data={"email": "jane.doe@example.com", "password": "mypassword"})
        self.assertEqual(res.status_code, 200)

        res_text = res.get_data(as_text=True)
        self.assertIn("That user does not exist!", res_text)

    def test_login_incorrect_password(self):
        create_user()

        res = self.app.post("/login", data={"email": "john.doe@example.com", "password": "abc"})
        self.assertEqual(res.status_code, 200)

        res_text = res.get_data(as_text=True)
        self.assertIn("Incorrect password!", res_text)

    def test_logout(self):
        create_user()

        self.app.post("/login", data={"email": "john.doe@example.com", "password": "mypassword"})

        res_logged_in = self.app.get("/")
        self.assertEqual(res_logged_in.status_code, 200)

        res_logged_out = self.app.get("/logout", follow_redirects=True)
        self.assertEqual(res_logged_in.status_code, 200)

        res_logged_out_text = res_logged_out.get_data(as_text=True)
        self.assertIn("Log In", res_logged_out_text)
