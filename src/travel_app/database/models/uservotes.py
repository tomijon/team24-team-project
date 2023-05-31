"""This module contains relevant classes and functions for user's up
and down votes.

Authors(s): Thomas,
"""
from enum import Enum

from database.database import _db
from database.models.country import Country
from database.models.user import User


class VoteType(Enum):
    """Enum representing the two types of vote"""
    UPVOTE = 1
    DOWNVOTE = 2


class UserVote(_db.Model):
    """User vote table for creating a many to many relationship.

    Fields:
    user_id -- the id of the user in the vote
    country_id -- the id of the country in the vote
    vote_id -- the id of the vote (1 for up vote, 2 for down vote)
    """
    __tablename__ = "user_votes"
    user_id = _db.Column(_db.Integer, _db.ForeignKey("users.id"),
                         primary_key=True)
    country_id = _db.Column(_db.Integer, _db.ForeignKey("countries.id"),
                            primary_key=True)
    vote_id = _db.Column(_db.Integer, nullable=False)


def add_vote(vote: UserVote):
    """Adds a UserVote to the database.

    Must be ran within app context.
    Must not be already in the database.

    Parameters:
        vote - the UserVote to add

    Errors:
        Can raise RuntimeError if vote for the user and country
            already exists.
    """
    if (get_user_vote(User.query.filter_by(id=vote.user_id).one(),
                      Country.query.filter_by(id=vote.country_id).one())
            != None):
        raise RuntimeError("Vote already exists for this user and country")
    _db.session.add(vote)
    _db.session.commit()


def remove_vote(vote: UserVote):
    """Removes a UserVote from the database.

    Must be ran within app context.
    If the vote is not in the database, this function does nothing.

    Parameters:
        vote - the UserVote to remove
    """
    if (get_user_vote(User.query.filter_by(id=vote.user_id).one(),
                      Country.query.filter_by(id=vote.country_id).one())
            != None):
        _db.session.delete(vote)
        _db.session.commit()
    

def get_user_vote(user:User, country: Country) -> VoteType:
    """Fetches the user's vote for the given country.

    Must be ran within app context.

    Parameters:
        user - The user in question
        country - The country to search for

    Returns:
        A VoteType object representing the vote case or None if no
        vote exists.
    """
    return UserVote.query.filter_by(
        user_id=user.id, country_id=country.id).first()


def get_votes(country: Country, vote_type: VoteType) -> list[UserVote]:
    """Find all votes of vote_type for this country.

    Must be ran within app context.

    Parameters:
        country - The country to find votes for.
        vote_type - The type of vote to find

    Returns a list containing all the votes of type vote_type
    """
    results = UserVote.query.filter_by(country_id=country.id,
                                       vote_id=vote_type.value).all()
    return results


def get_all_votes(country: Country) -> list[UserVote]:
    """Find all the votes for this country.

    Must be ran within app context.

    Parameters:
        country - The country to find votes for.

    Returns:
        A list containing all UserVote for the country.
    """
    return UserVote.query.filter_by(country_id=country.id).all()
    
