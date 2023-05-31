"""Form module for registering and logging in users.
Authors: Thomas,

"""
from flask_wtf import FlaskForm
from werkzeug.routing import ValidationError
from wtforms import *
from wtforms.validators import *


password_criteria = (
    """Passwords must:
    - Include a number
    - Include a lowercase character
    - Include an uppercase character
    - Include a special character
    - Be a minimum length of 8 characters
""")


def password_check(form, field):
    """Check the password meets the criteria.

    Passwords must:
     - Include a number
     - Include a lowercase character
     - Include an uppercase character
     - Include a special character
     - Be a minimum length of 8 characters

    Raises ValidationError if the above requirements are not met.
    """
    assert isinstance(form, RegisterForm), "Only required for registration"

    # Check length.
    if len(field.data) < 8:
        raise ValidationError(password_criteria)
    
    criteria = [
        lambda char: char.isdigit(),
        lambda char: char.islower(),
        lambda char: char.isupper(),
        lambda char: not (char.isalpha() or char.isdigit())]

    # Check all "Include" criteria
    for c in field.data:
        current = 0
        while current < len(criteria):
            if criteria[current](c) == True:
                criteria.pop(current)
            else:
                current += 1

    if len(criteria) > 1:
        raise ValidationError(password_criteria)


def no_specials(form, field):
    """Checks wether the field contains any special characters
    and raises ValidationError if it does.
    """
    for char in field.data:
        if not (char.isalpha() or char.isdigit()):
            raise ValidationError("Username must not contain symbols")


class RegisterForm(FlaskForm):
    """Registration form for new users. Does not include registration of
    admins."""
    username = StringField(validators=[DataRequired(), no_specials])
    password = PasswordField(validators=[DataRequired(), password_check])
    confirm_password = PasswordField(validators=[EqualTo('password', message="Passwords must match")])
    submit = SubmitField()


class LoginForm(FlaskForm):
    """Login form for existing users. Works for both admins and users."""
    username = StringField(validators=[DataRequired()])
    password = PasswordField(validators=[DataRequired()])
    submit = SubmitField()

class SearchForm(FlaskForm):
    """Search form for searching for countries."""
    search = StringField(validators=[DataRequired()])
    submit = SubmitField()

class CountryForm(FlaskForm):
    """Country form for editting country information."""
    name = StringField(validators=[DataRequired()])
    description = TextAreaField(validators=[DataRequired()])
    travel_advice = TextAreaField(validators=[DataRequired()])
    crime_index = FloatField(validators=[DataRequired()])
    disaster_risk = FloatField(validators=[DataRequired()])
    corruption_index = FloatField(validators=[DataRequired()])
    health = FloatField(validators=[DataRequired()])
    submit = SubmitField()
