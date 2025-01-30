"""Test module for the advice model.

Author(s): Thomas,
"""
from random import randint

from database.database import get_database
from conftest import app

db = get_database()

# Load model after database loading
from database.models.advice import *


# Fake user class
class FakeAdvice():
    def __init__(self, topic, description, link, id=9999):
        self.id = id
        self.topic = topic
        self.description = description
        self.link = link


def test_add_adivce_valid():
    """Test to determine if the add_advice function correctly adds an
    advice model to the database.
    """
    with app.app_context():
        advice = Advice(
            topic="test",
            description="test description",
            link="./"
            )
        add_advice(advice)
        result = get_advice_by_topic("test")
        remove_advice(advice)
        assert result != None, "Failed to add advice to the database"


def test_add_adivce_existing():
    """Test to determine if the add_advice function fails to add a
    second advice with the same topic.
    """
    with app.app_context():
        advice = Advice(
            topic="test",
            description="test description",
            link="./"
            )
        duplicate = Advice(
            topic="test",
            description="more test description",
            link="../"
            )
        add_advice(advice)
        try:
            add_advice(duplicate)
            remove_advice(duplicate)
        except:
            remove_advice(advice)
            return
        remove_advice(advice)
        raise AssertionError("Added 2 advice with the same topic")


def test_add_advice_wrong():
    """Test to determine if the add_advice function adds advice that is
    of the wrong type.
    """
    with app.app_context():
        fake_advice = FakeAdvice(
            "fake test",
            "fake test description",
            ".fakeadvice/")
        try:
            add_advice(fake_advice)
        except:
            return
        remove_advice(fake_advice)
        raise AssertionError("Added advice of wrong type to database")


def test_remove_advice():
    """Test to determine if the database correctly removes advice
    from the database.
    """
    with app.app_context():
        advice = Advice(
            topic="test",
            description="test description",
            link="./"
            )
        add_advice(advice)
        remove_advice(advice)
        assert get_advice_by_topic("test") == None, "Failed to remove advice"


def test_remove_advice_non_existing():
    """Test to make sure the remove_advice function does not fail if the
    advice passed is not in the database.
    """
    with app.app_context():
        advice = Advice(
            topic="test",
            description="test description",
            link="./"
            )
        try:
            remove_advice(advice)
        except:
            raise AssertionError("remove_advice should not fail")


def test_remove_adivce_wrong():
    """Test to make sure the database does not remove advice that is
    fake.
    """
    with app.app_context():
        advice = Advice(
            topic="test",
            description="test description",
            link="./"
            )
        fake_advice = FakeAdvice(
            advice.topic,
            advice.description,
            advice.link,
            advice.id)
        add_advice(advice)

        try:
            remove_advice(fake_advice)
        except:
            remove_advice(advice)
            return
        remove_advice(advice)
        raise AssertionError("Removed real advice using fake advice")


def test_get_advice_by_topic_existing():
    """Test to determine if the database successfully fetches the advice
    from the database.
    """
    with app.app_context():
        advice = Advice(
            topic="test",
            description="test description",
            link="./"
            )
        add_advice(advice)
        result = get_advice_by_topic("test") != None
        remove_advice(advice)
        assert result, "Failed to fetch advice"

        
def test_get_advice_by_topic_non_existing():
    """Test to determine if the database returns none when fetching
    advice that doesnt exist.
    """
    with app.app_context():
        advice = Advice(
            topic="test",
            description="test description",
            link="./"
            )
        add_advice(advice)
        result = get_advice_by_topic("test") != None
        remove_advice(advice)
        assert result, "Failed to fetch advice"

        
def test_get_advice_by_topic_wrong():
    """Test to determine if the get_advice_by_topic function accepts
    parameters that are not strings.
    """
    with app.app_context():
        try:
            get_advice_by_topic(12345)
        except:
            return
        raise AssertionError("get_advice_by_topic accepted incorrect parameter")
