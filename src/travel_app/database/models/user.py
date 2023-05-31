"""This module contains the model class for the user login information.

Author(s): Thomas, Renato
"""
from database.database import _db
from flask_login import UserMixin

from bcrypt import hashpw, gensalt, checkpw

class User(UserMixin, _db.Model):
    """Model class for user account details

    Fields:
    id -- the id of the user (primary key)
    username -- username for the user to login
    password -- password for the user
    role -- used for RBAC. Current roles are guest and admin
    """
    __tablename__ = "users"
    id = _db.Column(_db.Integer, primary_key=True, autoincrement=True)
    username = _db.Column(_db.String(32), nullable=False)
    password = _db.Column(_db.String(64), nullable=False)
    role = _db.Column(_db.String(16), nullable=False)

    def __init__(self, username, password, role="guest"):
        self.username = username
        self.password = hashpw(password.encode("utf-8"), salt=gensalt())
        self.role = role
        
    def set_role(self, role):
        """Set the role for the user"""
        assert role in ["guest", "admin"], "Unknown role"
        self.role = role        

    def __repr__(self):
        return f"User <{self.username}, {self.role}>"


def add_user(user: User):
    """Adds the user to the database.

    Must be ran within app context.
    Usernames must be unique.

    Parameters:
        user - the user to add.

    Errors:
        raises RuntimeError if username already exists.
    """
    if get_user_by_name(user.username) != None:
        raise RuntimeError("User already exists")
    _db.session.add(user)
    _db.session.commit()


def remove_user(user: User):
    """Removes the user from the database.

    Must be ran within app context.
    This function does nothing if the user does not exist already.

    Parameters:
        user - the User to remove
    """
    if User.query.filter_by(id=user.id).one_or_none() != None:
        _db.session.delete(user)
        _db.session.commit()


def get_user_by_name(username: str):
    """Fetch the user from the database with the given username.

    Must be ran within app context.

    Parameters:
        name - string representing the username of the user

    Returns the User object if one was found, otherwise None.
    """
    assert isinstance(username, str), "Username should be a string"
    result = User.query.filter_by(username=username).first()
    return result


def validate_user(username: str, password: str):
    """Determines if the password is correct for the user.

    Must be ran within app context.

    Parameters:
        username - The username of the user
        password - The password to check

    Returns:
        True if the username and password are correct.
    """
    user = get_user_by_name(username)

    if user == None:
        return False

    check_against = (user.password if isinstance(user.password, bytes) else
                     user.password.encode("utf-8"))
    return checkpw(password.encode("utf-8"), check_against)
    
