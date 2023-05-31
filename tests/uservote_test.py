"""Test module for the uservotes model.

Author(s): Thomas,
"""
from random import randint

from database.database import get_database
from conftest import app


db = get_database()

# Load model after database loading
from database.models.uservotes import *
from database.models.user import User, get_user_by_name
from database.models.country import Country, get_country_by_name


# FakeVote class used for testing.
class FakeVote():
    def __init__(self, user_id, country_id, vote_id):
        self.user_id = user_id
        self.country_id = country_id
        self.vote_id = vote_id
            

# Test data
test_user = None
test_country = None


def setup_module():
    """Adds test data to the database before tests are run"""
    global test_user
    global test_country

    print("Setting up uservote_test module...")
    
    # Set up test data.
    with app.app_context():    
        # Create test data and commit to the database.
        test_user = User(
            username=f"test_user{randint(1000, 9999)}",
            password=f"password{randint(1000, 9999)}",
            role="guest")
        username = test_user.username

        test_country = Country(
            name=f"test_country{randint(1000, 9999)}",
            description="Country for uservotes test",
            travel_advice="None",
            crime_index=0,
            disaster_risk=0,
            corruption_index=0,
            health=0)
        country_name = test_country.name
        
        db.session.add(test_user)
        db.session.add(test_country)
        db.session.commit()

        # Get test user and test_country.
        test_user = get_user_by_name(username)
        test_country = get_country_by_name(country_name)
    print("uservote_test module setup complete.")


def teardown_module():
    """Removes the test data from the database."""
    global test_user
    global test_country
    
    print("Tearing down uservote_test module...")

    with app.app_context():
        remove_vote(
            UserVote(
                user_id=test_user.id,
                country_id=test_country.id,
                vote_id=VoteType.UPVOTE.value)
            )
        remove_vote(
            UserVote(
                user_id=test_user.id,
                country_id=test_country.id,
                vote_id=VoteType.DOWNVOTE.value)
            )
        db.session.delete(test_user)
        db.session.delete(test_country)
        
        db.session.commit()

        test_user = None
        test_country = None
    print("Teardown successful.")


def test_add_vote():
    """A test to see if the add_vote function adds a valid vote to the
    database.
    """
    with app.app_context():
        vote = UserVote(
                user_id=test_user.id,
                country_id=test_country.id,
                vote_id=VoteType.UPVOTE.value
                )
        add_vote(vote)

        result = get_all_votes(test_country)
        remove_vote(vote)
    assert len(result) != 0, "Failed to add vote to the database"


def test_add_vote_existing():
    """A test to see if the add_vote function fails if there is
    already a vote in the database.
    """
    with app.app_context():
        vote1 = UserVote(
                user_id=test_user.id,
                country_id=test_country.id,
                vote_id=VoteType.UPVOTE.value
                )
        vote2 = UserVote(
                user_id=test_user.id,
                country_id=test_country.id,
                vote_id=VoteType.DOWNVOTE.value
                )
        add_vote(vote1)
        try:
            add_vote(vote2)
        except:
            remove_vote(vote1)
            return
        remove_vote(vote1)
        remove_vote(vote2)
        raise AssertionError("Added second vote but should have failed")
        


def test_add_invalid_type():
    """A test to see if the add_vote function adds an invalid object
    to the database.
    """
    with app.app_context():
        vote = "MY TEST VOTE"
        try:
            add_vote(vote)
            remove_vote(vote)
        except:
            return
        raise AssertionError("Vote should not have been added")


def test_add_invalid_vote():
    """A test to see if the add_vote function adds an invalid vote to
    the database (custom object version)."""
    with app.app_context():
        vote = FakeVote(test_user.id, test_country.id, VoteType.UPVOTE.value)
        try:
            add_vote(vote)
            remove_vote(vote)
        except:
            return
        raise AssertionError("Added FakeVote instead of breaking")


def test_remove_vote_existing():
    """A test to see if the remove_vote function successfully removes
    a vote from the database.
    """
    with app.app_context():
        vote = UserVote(
                user_id=test_user.id,
                country_id=test_country.id,
                vote_id=VoteType.UPVOTE.value
                )
        add_vote(vote)
        remove_vote(vote)
        assert len(get_all_votes(test_country)) == 0, "Failed to remove vote"


def test_remove_vote_none():
    """A test to see if the remove_vote function works if there is no
    vote to remove from the database.
    """
    with app.app_context():
        vote = UserVote(
                user_id=test_user.id,
                country_id=test_country.id,
                vote_id=VoteType.UPVOTE.value
                )
        try:
            remove_vote(vote)
        except:
            raise AssertionError("Remove function failed withnothing in"
                                 + "the database")


def test_remove_fake_vote():
    """A test to see if the remove_vote function fails if it is given
    a FakeVote object."""
    with app.app_context():
        vote = UserVote(
                user_id=test_user.id,
                country_id=test_country.id,
                vote_id=VoteType.UPVOTE.value
                )
        fake_vote = FakeVote(vote.user_id, vote.country_id, vote.vote_id)
        add_vote(vote)

        try:
            remove_vote(fake_vote)
        except:
            remove_vote(vote)
            return

        remove_vote(vote)
        assert len(get_all_votes(test_country)) == 1, "Removed fake vote"
            

def test_get_user_vote_existing():
    """A test to see if the get_user_vote function returns the vote
    for the given user and country when it exists.
    """
    with app.app_context():
        vote = UserVote(
                user_id=test_user.id,
                country_id=test_country.id,
                vote_id=VoteType.UPVOTE.value
                )
        add_vote(vote)

        result = get_user_vote(test_user, test_country)
        remove_vote(vote)
        assert result != None, "Vote not found"


def test_get_user_vote_none():
    """A test to see if the get_user_vote function returns none when
    there are no votes to find.
    """
    with app.app_context():
        assert get_user_vote(test_user, test_country) == None, (
            "Found a vote that shouldn't exist")


def test_get_user_vote_wrong():
    """A test to see if the get_user_vote function works when
    incorrect parameters are given.
    """
    with app.app_context():
        try:
            get_user_vote("fake_user", "fake_country")
        except:
            return
        raise AssertionError("get_user_vote function accepted incorrect "
                             + "parameters")


def test_get_upvotes():
    """A test to see if the get_votes function returns all the
    upvotes for a country.
    """
    with app.app_context():
        vote = UserVote(
                user_id=test_user.id,
                country_id=test_country.id,
                vote_id=VoteType.UPVOTE.value
                )
        add_vote(vote)

        result = get_votes(test_country, VoteType.UPVOTE)
        remove_vote(vote)
        assert len(result) == 1, "Failed to correctly get all upvotes"


def test_get_downvotes():
    """A test to see if the get_votes function returns all the
    upvotes for a country.
    """
    with app.app_context():
        vote = UserVote(
                user_id=test_user.id,
                country_id=test_country.id,
                vote_id=VoteType.DOWNVOTE.value
                )
        add_vote(vote)

        result = get_votes(test_country, VoteType.DOWNVOTE)
        remove_vote(vote)
        assert len(result) == 1, "Failed to correctly get all downvotes"


def test_get_votes_invalid():
    """A test to see if the get_votes function fails when given
    invalid parameters.
    """
    with app.app_context():
        try:
            get_votes("test_country")
        except:
            return
        raise AssertionError("get_votes function should have failed")


def test_get_all_votes():
    """A test to see if the get_all_votes function returns all the
    votes for the country.
    """
    with app.app_context():
        assert len(get_all_votes(test_country)) == 0, ("Found votes for country"
                                                       + " that don't exist")
