from os import getenv

from database.database import load_database, create_tables, get_database
from dotenv import load_dotenv
from flask import Flask, render_template
from werkzeug.exceptions import HTTPException

load_dotenv()
app = Flask(__name__)

# Setup app config
app.config["DB_ADDRESS"] = getenv("DB_ADDRESS")
app.config["DB_PORT"] = int(getenv("DB_PORT"))
app.config["DB_NAME"] = getenv("DB_NAME")
app.config["DB_USERNAME"] = getenv("DB_USERNAME")
app.config["DB_PASSWORD"] = getenv("DB_PASSWORD")

app.config['SECRET_KEY'] = getenv("SECRET_KEY")

# Setup sqlalchemy side of app config
##app.config["SQLALCHEMY_DATABASE_URI"] = (f"mysql://"
##                                         + app.config["DB_USERNAME"] + ":"
##                                         + app.config["DB_PASSWORD"] + "@"
##                                         + app.config["DB_ADDRESS"] + ":"
##                                         + str(app.config["DB_PORT"]) + "/"
##                                         + app.config["DB_NAME"])
app.config["SQLALCHEMY_DATABASE_URI"] = ("sqlite:///:memory:")
app.config['SQLALCHEMY_ECHO'] = getenv("SQLALCHEMY_ECHO") == "True"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = (
    getenv("SQLALCHEMY_TRACK_MODIFICATIONS") == "True")

load_database(app)
from main.views import main_blueprint, map_blueprint, admin_blueprint, country_blueprint, search_blueprint, login_blueprint, register_blueprint


from session import login_manager
login_manager.init_app(app)

app.register_blueprint(main_blueprint)
app.register_blueprint(map_blueprint)
app.register_blueprint(admin_blueprint)
app.register_blueprint(country_blueprint)
app.register_blueprint(search_blueprint)
app.register_blueprint(login_blueprint)
app.register_blueprint(register_blueprint)

create_tables(app)

# Error Handling
@app.errorhandler(HTTPException)
def render_error(error):
    error = str(error)
    errno = error[:3]
    error = error[4:]
    name = error.split(": ")[0]
    message = error.split(": ")[1]
    return render_template("error.html",
                           errno=errno,
                           error=error,
                           message=message)


if __name__ == "__main__":
    from database.models.advice import Advice
    from database.models.country import Country
    from database.models.countryadvice import CountryAdvice
    from database.models.user import User
    import csv

    with app.app_context():
        
        db = get_database()


        # Do this for each model.
        with open("advice.csv") as file:
            reader = csv.reader(file)
            header = next(reader)

            for row in reader:
                details = dict(zip(header, row))
                item = Advice(**details)

                db.session.add(item)
                # db.session.commit() # Add it here to commit after every addition
            db.session.commit()

        # Do this for each model.
        with open("country_advice.csv") as file:
            reader = csv.reader(file)
            header = next(reader)

            for row in reader:
                details = dict(zip(header, row))
                item = CountryAdvice(**details)

                db.session.add(item)
                # db.session.commit() # Add it here to commit after every addition
            db.session.commit()

        # Do this for each model.
        with open("countries.csv") as file:
            reader = csv.reader(file)
            header = next(reader)

            for row in reader:
                details = dict(zip(header, row))
                item = Country(**details)

                db.session.add(item)
                # db.session.commit() # Add it here to commit after every addition
            db.session.commit()

        admin = User("admin", "password", "admin")
        db.session.add(admin)
        db.session.commit()

    app.run()
