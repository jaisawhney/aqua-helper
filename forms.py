from flask_wtf import FlaskForm
from wtforms import StringField, EmailField, PasswordField, TextAreaField, DateField, SubmitField, DateTimeField, \
    IntegerField
from wtforms.validators import DataRequired, ValidationError
from wtforms_sqlalchemy.fields import QuerySelectField
from werkzeug.security import check_password_hash

from models import User, Aquarium


class LoginForm(FlaskForm):
    email = EmailField("Email", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Submit")

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if not user:
            raise ValidationError("That user does not exist!")

    def validate_password(self, password):
        user = User.query.filter_by(email=self.email.data).first()
        if user and not check_password_hash(user.password, password.data):
            raise ValidationError("That password does not match the user!")


class SignupForm(FlaskForm):
    email = EmailField("Email", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Submit")

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError("That email is already being used!")


class AquariumForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired()])
    submit = SubmitField("Submit")


class AquariumLivestockForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired()])
    quantity = IntegerField("Quantity", validators=[DataRequired()])
    added_on = DateField("Added On", validators=[DataRequired()])
    submit = SubmitField("Submit")


class AquariumActionsForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired()])
    description = TextAreaField("Description", validators=[DataRequired()])
    due_on = DateField("Date Due", validators=[DataRequired()])
    submit = SubmitField("Submit")
