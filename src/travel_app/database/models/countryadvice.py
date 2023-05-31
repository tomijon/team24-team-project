"""This module defines the model class used to provide a many to many
relationship between countries and advice for the country.

Author(s): Thomas,
"""

from database.database import _db
from database.models.country import Country
from database.models.advice import Advice


class CountryAdvice(_db.Model):
    """Model class for determining a relationship betweeen a country
    and advice.

    Fields:
    country_id -- id of the country the advice applies to
    advice_id -- the advice for the country
    """
    __tablename__ = "country_advice"
    country_id = _db.Column(_db.Integer, _db.ForeignKey("countries.id"),
                            primary_key=True)
    advice_id = _db.Column(_db.Integer, _db.ForeignKey("advice.id"),
                           primary_key=True)

    def __repr__(self):
        return f"CountryAdvice <{self.country_id}, {self.advice_id}>"

      
def get_advice(country: Country) -> list[Advice]:
    """Fetches all the advice for the country.

    Must be ran within app context.

    Parameters:
        country - The country to get advice for

    Returns:
        A list of Advice objects related to the country
    """
    assert isinstance(country, Country)
    advice_ids = [advice.advice_id for advice in CountryAdvice.query.filter_by(
        country_id=country.id).all()]
    advice = [Advice.query.filter_by(id=advice_id).one()
              for advice_id in advice_ids]
    return advice    


def add_country_advice(country: Country, advice: Advice):
    """Adds a new relationship between the country and some advice

    Must be ran within app context.

    Parameters:
        country - The country in the relationship
        advice - The advice in the relationship
    """
    assert isinstance(country, Country)
    assert isinstance(advice, Advice)
    
    if (CountryAdvice.query.filter_by(
            country_id=country.id, advice_id=advice.id).first()):
        raise RuntimeError("Relationship already exists")
    
    country_advice = CountryAdvice(
        country_id=country.id,
        advice_id=advice.id)
    _db.session.add(country_advice)
    _db.session.commit()


def remove_country_advice(country: Country, advice: Advice):
    """Removes the country advice relationship.

    Must be ran within app context.
    This function does nothing if there is no relationship present.

    Parameters:
        country - The country in the relationship
        advice - The advice in the relationship
    """
    assert isinstance(country, Country)
    assert isinstance(advice, Advice)
    country_advice = CountryAdvice.query.filter_by(
        country_id=country.id,
        advice_id=advice.id).one_or_none()
    if country_advice:
        _db.session.delete(country_advice)
        _db.session.commit()

