"""Test module for the users model.

Author(s): Thomas,
"""
from random import randint

from database.database import get_database
from conftest import app

db = get_database()

# Load model after database loading
from database.models.user import *


# Fake user class
class FakeUser():
    def __init__(self, username, password):
        self.id = 9999
        self.username = username
        self.password = password
        self.role = "guest"
        

# Test data
test_user = None
username = None
password = None


def setup_module():
    """Adds test data to the database before tests are run"""
    global test_user
    global username
    global password

    print("Setting up user_test module...")
    
    # Set up test data.
    with app.app_context():
        username = f"test_user{randint(1000, 9999)}"
        password = f"password{randint(1000, 9999)}"
        
        # Create test data and commit to the database.
        test_user = User(
            username=username,
            password=password,
            role="guest")
        
        db.session.add(test_user)
        db.session.commit()

        # Get test user and test_country.
        test_user = get_user_by_name(username)
    print("user_test module setup complete.")


def teardown_module():
    """Removes the test data from the database."""
    global test_user

    print("Tearing down user_test module...")

    with app.app_context():
        db.session.delete(test_user)
        db.session.commit()

    test_user = None
    print("Teardown successful.")


def test_add_user_valid():
    """Tests the add_user function to make sure it can add a user."""
    with app.app_context():
        user = User(
            username="no_one",
            password="no_ones_password",
            role="guest")
        try:
            add_user(user)
            remove_user(user)
        except:
            raise AssertionError("Failed to add user to the database")


def test_add_user_invalid():
    """Tests the add_user function to make sure it doesnt add fake
    user objects.
    """
    with app.app_context():
        fake_user = FakeUser("imposter",
                             "IWantYourPassword")
        try:
            add_user(fake_user)
            remove_user(fake_user)
        except:
            return
        raise AssertionError("Succeeded in adding a fake user")


def test_add_existing():
    """Tests wether the add_user function prevents adding 2 users with
    the same username.
    """
    with app.app_context():
        duplicate = User(
            username=username,
            password=password,
            role="guest")
        try:
            add_user(duplicate)
            remove_user(duplicate)
        except:
            return
        raise AssertionError("Should not have added user with duplicate"
                             + " username")


def test_remove_existing():
    """Tests wether the remove_user function successfully removes a
    user from the database.
    """
    with app.app_context():
        user = User(
            username="delete_me",
            password="password"
            )
        add_user(user)
        remove_user(get_user_by_name("delete_me"))
        assert get_user_by_name("delete_me") == None, "Failed to delete user"


def test_remove_none():
    """Test to determine if the remove_user function fails if the user
    does not exist in the database.
    """
    with app.app_context():
        user = User(
            username="delete_me",
            password="password"
            )
        try:
            remove_user(user)
        except:
            raise AssertionError("Remove function should not fail if user "
                                 + "does not exist.")


def test_get_user_by_name_existing():
    """Test to determine if the get_user_by_name function successfully
    returns the test user.
    """
    with app.app_context():
        assert get_user_by_name(username).id == test_user.id, (
            "Failed to find the test user")


def test_get_user_by_name_none():
    """Test to determine if the get_user_by_name function successfully
    returns none when the username is not in the database.
    """
    with app.app_context():
        assert get_user_by_name("dhwauidhiawuhdiawhdiua") == None, (
            "Found user that doesn't exist")


def test_get_user_by_name_wrong():
    """Test to determine if the get_user_by_name function works with
    arguments that aren't acceptible.
    """
    with app.app_context():
        try:
            get_user_by_name(1234)
        except:
            return
        raise AssertionError("get_user_by_name function worked for int "
                             + "parameter")


def test_validate_user_correct():
    """A test to determine if the validation function correctly
    validates a user.
    """
    with app.app_context():
        assert validate_user(username, password), "Failed to validate"


def test_validate_user_incorrect():
    """A test to determine if the validation function returns false
    when given incorrect information.
    """
    with app.app_context():
        assert validate_user(username, "wrong_password") == False, (
            "Validated incorrect information")


def test_validate_user_wrong():
    """A test to determine if the validation function fails when
    given parameters of incorrect type.
    """
    with app.app_context():
        try:
            validate_user(12234, True)
        except:
            return
        raise AssertionError("validate user should have failed")
