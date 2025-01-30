"""This module contains the model class for the country information
table.

Author(s): Thomas,
"""
from flask import Flask

from database.database import _db


class Country(_db.Model):
    """Model class for country information.

    Fields:
    id -- The id of the country (primary key)
    name -- The name of the country
    description -- Information about the country.
    travel_advice -- The summary of the travel advice (whether the
        country should be travelled to)
    crime_index -- The level of crime in the country (higher means
        more crime)
    disaster_risk -- The severity and risk of disasters that happen in
        said country (higher means worse disasters)
    corrpution_index -- How corrupt a country is (higher means more)
    health -- The level of healthcare in the country (higher means
        better)
    """
    __tablename__ = "countries"
    id = _db.Column(_db.Integer, primary_key=True, autoincrement=True)
    name = _db.Column(_db.String(64), nullable=False)
    description = _db.Column(_db.String(2048), nullable=False)
    travel_advice = _db.Column(_db.String(256), nullable=False)
    crime_index = _db.Column(_db.Float, default=0.0)
    disaster_risk = _db.Column(_db.Float, default=0.0)
    corruption_index = _db.Column(_db.Float, default=0.0)
    health = _db.Column(_db.Float, default=0.0)

    def __eq__(self, other):
        assert isinstance(other, Country)
        return self.id == other.id

    def __hash__(self):
        return self.id
        
    def __repr__(self):
        return f"Country <{self.name}>"


def all_country_names() -> list[str]:
    """Fetch all the country names from the database.

    Must be ran within app context.

    Returns a list of strings containing every name.
    """
    results = Country.query.all()
    if results:
        results = [country.name for country in Country.query.all()]
    return results


def get_country_by_name(name: str) -> Country:
    """Fetch the country from the database with the given name.

    Must be ran within app context.

    Parameters:
        name - string representing the name of the country

    Returns the country object if one was found, otherwise None.
    """
    result = Country.query.filter_by(name=name).first()
    return result


def get_all_countries() -> set:
    """Fetch all the countries from the database.

    Returns:
        Returns all the countries as part of a set.
    """
    return set(Country.query.all())

  
def remove_country(country: Country):
    """Removes a country from the database.

    Must be ran within app context.
    Checks country is in the database before attempting removal.
    Also deletes all user votes and country advice alongside it.

    Parameters:
        country - the country to remove
    """
    # Check country in db before continuing.
    in_db = Country.query.filter_by(id=country.id) != None
    if not in_db:
        return

    # Remove all user votes.
    from database.models.uservotes import get_all_votes, remove_vote
    for vote in get_all_votes(country):
        remove_vote(vote)

    # Remove all country advice.
    from database.models.countryadvice import get_advice, remove_country_advice
    for advice in get_advice(country):
        remove_country_advice(country, advice)

    # Remove country.
    _db.session.delete(country)
    _db.session.commit()


def add_country(country: Country):
    """Adds a country to the database.

    Must be ran within app context.
    There is no checking if a country exists. The primary key is the
    id of the country. Two separate countries with the same name can
    exist.

    Parameters:
        country - the country to add
    """
    _db.session.add(country)
    _db.session.commit()

