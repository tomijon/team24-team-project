"""Test module for the country advice model.

Author(s): Thomas,
"""
from random import randint

from database.database import get_database
from conftest import app


db = get_database()

# Load model after database loading
from database.models.countryadvice import *
from database.models.advice import Advice, get_advice_by_topic
from database.models.country import Country, get_country_by_name            


# Class used to make fake advice/country instances.
class IdClass():
    def __init__(self, id):
        self.id = id

# Test data
test_advice = None
test_country = None


def setup_module():
    """Adds test data to the database before tests are run"""
    global test_advice
    global test_country

    print("Setting up countryadvice_test module...")
    
    # Set up test data.
    with app.app_context():    
        # Create test data and commit to the database.
        test_advice = Advice(
            topic="test_topic",
            description="Description about test topic",
            link="./")

        test_country = Country(
            name=f"test_country{randint(1000, 9999)}",
            description="Country for uservotes test",
            travel_advice="None",
            crime_index=0,
            disaster_risk=0,
            corruption_index=0,
            health=0)
        country_name = test_country.name
        
        db.session.add(test_advice)
        db.session.add(test_country)
        db.session.commit()

        # Get test user and test_country.
        test_advice = get_advice_by_topic("test_topic")
        test_country = get_country_by_name(country_name)
    print("countryadvice_test module setup complete.")


def teardown_module():
    """Removes the test data from the database."""
    global test_advice
    global test_country
    
    print("Tearing down countryadvice_test module...")

    with app.app_context():
        remove_country_advice(test_country, test_advice)
        
        db.session.delete(test_advice)
        db.session.delete(test_country)
        db.session.commit()

        test_advice = None
        test_country = None
    print("Teardown successful.")


def test_add_country_advice_valid():
    """A test to determine if the add_country_advice function
    successfully adds a relationship to the database.
    """
    with app.app_context():
        add_country_advice(test_country, test_advice)
        result = len(get_advice(test_country)) == 1
        remove_country_advice(test_country, test_advice)
        assert result, "Could not add advice to the database"


def test_add_country_advice_existing():
    """A test to determine if the add_country_advice function adds
    a relationship to the database that already exists.
    """
    with app.app_context():
        add_country_advice(test_country, test_advice)
        try:
            add_country_advice(test_country, test_advice)
        except:
            remove_country_advice(test_country, test_advice)
            return

        remove_country_advice(test_country, test_advice)
        raise AssertionError("Added country advice twice")


def test_add_country_advice_wrong():
    """A test to determine if the add_country_advice function accepts
    incorrect parameters.
    """
    with app.app_context():
        try:
            add_country_advice(12, 34)
            remove_country_advice(12, 34)
        except:
            return

        raise AssertionError("Added country advice with int parameters")


def test_remove_country_advice_existing():
    """A test to determine if the remove_country_advice function
    removes advice relationship.
    """
    with app.app_context():
        add_country_advice(test_country, test_advice)
        total = len(get_advice(test_country))
        remove_country_advice(test_country, test_advice)
        assert total - len(get_advice(test_country)) == 1, "Failed to remove relationship"


def test_remove_country_advice_non_existing():
    """A test to determine if the remove_country_advice function
    fails when trying to remove a relationship that does not exist.
    """
    with app.app_context():
        try:
            remove_country_advice(test_country, test_advice)
        except:
            raise AssertionError("Remove country function should not fail")


def test_remove_country_advice_wrong():
    """A test to determine if the remove_country_advice function
    accepts wrong parameters.
    """
    with app.app_context():
        add_country_advice(test_country, test_advice)
        country = IdClass(test_country.id)
        advice = IdClass(test_advice.id)
        try:
            remove_country_advice(country, advice)
        except:
            remove_country_advice(test_country, test_advice)
            return

        remove_country_advice(test_country, test_advice)
        raise AssertionError("Function accepted parameters of incorrect type""")

    
def test_get_advice():
    """A test to determine if the get_advice function returns the
    correct amount of relationships.
    """
    with app.app_context():
        assert len(get_advice(test_country)) == 0, (
            "Found data that shouldn't exist")
        add_country_advice(test_country, test_advice)
        result = len(get_advice(test_country)) == 1
        remove_country_advice(test_country, test_advice)
        assert result, "Should have counted 1 relationship"


def test_get_advice_wrong():
    """A test to determine if the get_advice function accepts
    parameters of incorrect type."""
    with app.app_context():
        add_country_advice(test_country, test_advice)
        country = IdClass(test_country.id)
        try:
            get_advice(country)
        except:
            return
        remove_country_advice(test_country, test_advice)
        raise AssertionError("get_advice function accepted incorrect "
                             + "parameters")
