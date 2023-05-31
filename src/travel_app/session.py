"""Module for tracking the session of the user.

Contains functions for controlling access and for managing the session.
Authors: Thomas,
"""
from functools import wraps
from flask_login import current_user
from flask_login import LoginManager
from flask import abort, flash, redirect, url_for
from database.models.user import User


def role_required(*roles):
    """Decorator for checking whether a user has the correct access
    rights.

    If the user does not have the correct access rights, they are redirected to main and flashed an error message.

    If the user is not logged in, they are redirected to the login page and flashed a error message.

    The function is run only if the user is authenticated with the
    correct role.
    """
    def perform_check(func):
        @wraps(func)
        def execute(*args, **kwargs):
            if current_user.is_authenticated:
                # Only run function if access allowed
                print("user role: ", current_user.role)
                if current_user.role in roles:
                    return func(*args, **kwargs)
                else:
                    flash(f'You do not have the correct credentials for this page.', 'error')
                    return redirect(url_for('main.index'))
            else:
                flash(f'The page you are attempting to access requires you to login', 'warning')
                return redirect(url_for('login.login'))
        return execute
    return perform_check


login_manager = LoginManager()
login_manager.login_view = "login.login"

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))