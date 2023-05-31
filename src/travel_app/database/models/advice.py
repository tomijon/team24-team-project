"""This module defines the model class used to define advise.

Advise can be for any of the following:
    - crime
    - disasters
    - health

Author(s): Thomas,
"""

from database.database import _db


class Advice(_db.Model):
    """Advice model for defining advice about a certain topic.

    Fields:
    id -- advice id (primary key)
    topic -- the topic name for the advice
    description -- description of the topic
    link -- link to a helpful video
    """
    __tablename__ = "advice"
    id = _db.Column(_db.Integer, primary_key=True, autoincrement=True)
    topic = _db.Column(_db.String(64), nullable=False)
    description = _db.Column(_db.String(512), nullable=False)
    link = _db.Column(_db.String(256), nullable=True)    


def add_advice(advice: Advice):
    """Adds an advice object to the Advice table.

    Must be ran within app context.
    Cannot have the same topic as an Advice that already exists.

    Parameters:
        advice - The Advice object to add.
    """
    assert get_advice_by_topic(advice.topic) == None, "Advice already exists"
    _db.session.add(advice)
    _db.session.commit()


def remove_advice(advice: Advice):
    """Removes an advice object from the Advice table.

    Must be ran within app context.
    This function does nothing if the advice does not exist.

    Parameters:
        advice - The Advice object to remove.
    """
    if get_advice_by_topic(advice.topic):
        _db.session.delete(advice)
        _db.session.commit()


def get_advice_by_topic(topic: str) -> Advice:
    """Find an Advice object based on the topic given.

    Must be ran within app context.

    Parameters:
        topic - str representing the topic
    """
    assert isinstance(topic, str), "Expected str for topic"
    return Advice.query.filter_by(topic=topic).one_or_none()

    
