"""Module to load the database before running tests.

Author(s): Thomas,
"""
from database.database import load_database, create_tables
from flask import Flask

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"
app.config["SQLALCHEMY_ECHO"] = False
app.config["SQLALCHEMY_TRACK_DATABASE_MODIFICATIONS"] = False

load_database(app)
create_tables(app)
