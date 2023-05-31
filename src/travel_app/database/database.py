"""This module contains the database object and provides functions for
operating on the database object

Author(s): Thomas,
"""
from flask_sqlalchemy import SQLAlchemy

# Module variables.
_db = None


def load_database(app):
    """Loads the database connection for the app session into the _db
    variable.

    Parameters:
    app -- The flask session app that the database will apply to.

    Returns:
    	True if the database was successfully instantiated.
    """
    global _db
    assert _db == None, "Database instance already created."
    _db = SQLAlchemy(app)
    return True


def get_database():
    """Get the database for the session.

    Only use if necessary.

    Returns:
    	The database instance
    """
    global _db
    return _db


def drop_tables(app):
    """Drops all the tables in the database.

    ONLY USE THIS IF YOU ARE SURE YOU WANT TO ERASE ALL DATA IN THE
    DATABASE.
    """
    with app.app_context():
        _db.drop_all()
        

def create_tables(app):
    """Creates all the tables in the database based on the imported
    models.

    This does not overwrite existing tables in the database.

    Returns:
    	True if the operation was successful.
    """
    from database.models.country import Country
    from database.models.user import User
    from database.models.uservotes import UserVote
    from database.models.advice import Advice
    from database.models.countryadvice import CountryAdvice
    with app.app_context():
    	_db.create_all()
    return True
