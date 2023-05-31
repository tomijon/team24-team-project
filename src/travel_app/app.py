from os import getenv

from database.database import load_database, create_tables
from dotenv import load_dotenv
from flask import Flask, render_template
from werkzeug.exceptions import HTTPException

load_dotenv()
app = Flask(__name__)

# Setup app config
app.config['SECRET_KEY'] = getenv("SECRET_KEY")

# Setup sqlalchemy side of app config
app.config["SQLALCHEMY_DATABASE_URI"] = (f"sqlite:///travel_advice")
app.config['SQLALCHEMY_ECHO'] = getenv("SQLALCHEMY_ECHO") == "True"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = (
        getenv("SQLALCHEMY_TRACK_MODIFICATIONS") == "True")

load_database(app)
from main.views import main_blueprint, map_blueprint, admin_blueprint, \
    country_blueprint, search_blueprint, login_blueprint, register_blueprint


from session import login_manager

login_manager.init_app(app)

app.register_blueprint(main_blueprint)
app.register_blueprint(map_blueprint)
app.register_blueprint(admin_blueprint)
app.register_blueprint(country_blueprint)
app.register_blueprint(search_blueprint)
app.register_blueprint(login_blueprint)
app.register_blueprint(register_blueprint)


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
    app.run()
