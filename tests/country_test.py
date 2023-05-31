"""Test module for the country model.

Author(s): Thomas,
"""
from random import randint
from dataclasses import dataclass

from database.database import get_database
from conftest import app

db = get_database()

# Load model after database loading
from database.models.country import *


# Fake country class
@dataclass
class FakeCountry():
    id: int
    name: str
    description: str
    travel_advice: str
    crime_index: float
    disaster_risk: float
    corruption_index: float
    health: float


def test_add_country():
    """Test to make sure the database correctly adds a valid country to
    the database.
    """
    with app.app_context():
        country = Country(
            name="test_country",
            description="test_description",
            travel_advice="don't travel here",
            crime_index=0.5,
            disaster_risk=0.5,
            corruption_index=0.5,
            health=0.5)

        add_country(country)
        result = get_country_by_name("test_country") != None
        remove_country(country)
        assert result == True, "Failed to add country."


def test_add_country_wrong():
    """Test to make sure the add_country function does not accept fake
    country models.
    """
    with app.app_context():
        country = FakeCountry(
            10,
            "test_country",
            "test_description",
            "don't travel here",
            0.5,
            0.5,
            0.5,
            0.5)

        try:
            add_country(country)
        except:
            return

        remove_country(country)
        raise AssertionError("Managed to add fake country to database")


def test_remove_country_existing():
    """Test to make sure the remove_country function removes countries
    that exist.
    """
    with app.app_context():
        country = Country(
            name="test_country",
            description="test_description",
            travel_advice="don't travel here",
            crime_index=0.5,
            disaster_risk=0.5,
            corruption_index=0.5,
            health=0.5)

        add_country(country)
        remove_country(country)
        result = get_country_by_name("test_country") == None
        assert result == True, "Failed to remove country."


def test_remove_country_non_existing():
    """Test to make sure the remove_country function does not fail
    when removing countries that don't exist.
    """
    with app.app_context():
        country = Country(
            name="test_country",
            description="test_description",
            travel_advice="don't travel here",
            crime_index=0.5,
            disaster_risk=0.5,
            corruption_index=0.5,
            health=0.5)

        try:
            remove_country(country)
            return
        except:
            raise AssertionError("remove_country should fail silently")


def test_remove_country_wrong():
    """Test to make sure the remove_country function does not accept
    fake country models.
    """
    with app.app_context():
        country = FakeCountry(
            10,
            "test_country",
            "test_description",
            "don't travel here",
            0.5,
            0.5,
            0.5,
            0.5)

        try:
            remove_country(country)
            return
        except:
            raise AssertionError("remove_country should not accept fake country"
                                 + " models.")


def test_get_country_by_name_existing():
    """Test to make sure the test_get_country_by_name function
    successfully returns the country.
    """
    with app.app_context():
        country = Country(
            name="test_country",
            description="test_description",
            travel_advice="don't travel here",
            crime_index=0.5,
            disaster_risk=0.5,
            corruption_index=0.5,
            health=0.5)

        add_country(country)
        result = get_country_by_name("test_country") != None
        remove_country(country)
        assert result == True, "Failed to fetch country."


def test_get_country_by_name_non_existing():
    """Test to make sure the test_get_country_by_name function
    returns None when it cannot find the country in the database.
    """
    with app.app_context():
        assert get_country_by_name("nothing") == None, (
            "Found country that doesn't exist")


def test_get_country_by_name_wrong():
    """Test to make sure the test_get_country_by_name function
    only accepts strings.
    """
    with app.app_context():
        try:
            get_country_by_name(1234)
        except:
            raise AssertionError("get_country_by_name function accepted "
                                 + "parameters of incorrect type.")
        
