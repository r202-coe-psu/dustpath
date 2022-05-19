from dustpath import models

from wtforms import PasswordField, validators, StringField
from flask_mongoengine.wtf import model_form
from flask_wtf import FlaskForm

BaseRegisterForm = model_form(
    models.User,
    FlaskForm,
    exclude=["status", "roles", "created_date", "updated_date"],
    field_args={
        "username": {"label": "Username"},
        "first_name": {"label": "Firstname"},
        "last_name": {"label": "Lastname"},
    },
)


class RegisterForm(BaseRegisterForm):
    email = StringField(
        "Email Address", validators=[validators.InputRequired(), validators.Email()]
    )

    password = PasswordField(
        "Password", validators=[validators.InputRequired(), validators.Length(min=6)]
    )
    confirm_password = PasswordField(
        "Confirm Password",
        validators=[
            validators.InputRequired(),
            validators.Length(min=6),
            validators.EqualTo("password", message="""password mismatch"""),
        ],
    )


BaseLoginForm = model_form(
    models.User,
    FlaskForm,
    field_args={"username": {"label": "Username"}},
    only=["username", "password"],
)


class LoginForm(BaseLoginForm):
    password = PasswordField(
        "Password", validators=[validators.InputRequired(), validators.Length(min=6)]
    )
