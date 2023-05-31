"""Module for app routes to webpages.

Author(s): Thomas, Renato, Cameron
"""
from werkzeug.security import generate_password_hash, check_password_hash
from users.forms import *
from database.database import get_database
from database.models.country import get_country_by_name
from database.models import uservotes as uv
from database.models.user import *
from database.models.countryadvice import get_advice
from flask import *
from flask_login import login_user, logout_user, login_required, current_user
from session import role_required

main_blueprint = Blueprint('main', __name__, template_folder='templates')
map_blueprint = Blueprint('map', __name__, template_folder='templates')
admin_blueprint = Blueprint('admin', __name__, template_folder='templates')
country_blueprint = Blueprint('country', __name__, template_folder='templates')
search_blueprint = Blueprint('search', __name__, template_folder='templates')
login_blueprint = Blueprint('login', __name__, template_folder='templates')
register_blueprint = Blueprint('register', __name__,
                               template_folder='templates')

isSearch = True
country = None

@main_blueprint.route('/')
def index():
    return render_template('main/homepage.html')


@map_blueprint.route('/map')
def map():
    return render_template('main/map.html')


@admin_blueprint.route('/admin', methods=['GET', 'POST'])
@role_required('admin')
@login_required
def admin():
    global isSearch
    global country

    search_form = SearchForm()
    country_form = CountryForm()

    # Render the search form if in search mode.
    if isSearch:
        # Search for the country.
        if search_form.validate_on_submit():
            country = get_country_by_name(search_form.search.data.lower())

            # If no country was found, render search bar.
            if not country:
                return render_template(
                    'main/admin.html',
                    search_form=search_form,
                    country_form=None
                )

            isSearch = False
            country_form.name.data = country.name
            country_form.description.data = country.description
            country_form.travel_advice.data = country.travel_advice
            country_form.crime_index.data = country.crime_index
            country_form.disaster_risk.data = country.disaster_risk
            country_form.corruption_index.data = country.corruption_index
            country_form.health.data = country.health

            return render_template(
                "main/admin.html",
                search_form=None,
                country_form=country_form)
        else:
            return render_template(
                'main/admin.html',
                search_form=search_form,
                country_form=None)

    # If in edit mode.
    else:
        if country_form.validate_on_submit():
            country.name = country_form.name.data,
            country.description = country_form.description.data,
            country.travel_advice = country_form.travel_advice.data,
            country.crime_index = country_form.crime_index.data,
            country.disaster_risk = country_form.disaster_risk.data,
            country.corruption_index = country_form.corruption_index.data,
            country.health = country_form.health.data
            get_database().session.merge(country)
            get_database().session.commit()
            isSearch = True

            return render_template(
                "main/admin.html",
                search_form=search_form,
                country_form=None)
        else:
            return render_template(
                "main/admin.html",
                search_form=None,
                country_form=country_form)

                
@admin_blueprint.route('/country')
def country():
    return render_template('main/country.html')


@country_blueprint.route('/search', methods=['GET', 'POST'])
def search():
    """ Search for a country by name.
    If the country is not found, flash a message and return to the
    search page.
    If the country is found, display the country information on the
    country page.
    """
    form = SearchForm()
    if form.validate_on_submit():
        country = get_country_by_name(form.search.data.lower())
        if country is not None:
            return redirect(f"/country/{country.name}")
        flash(f'Country "{form.search.data}" not found. Please try again.',
              'warning')
    return render_template('main/search.html', form=form)


@country_blueprint.route('/country/<country_name>')
def show_country(country_name):
    """Render the country information to the webpage."""
    country = get_country_by_name(country_name)
    if country:
        upvotes = len(uv.get_votes(country, uv.VoteType.UPVOTE))
        downvotes = len(uv.get_votes(country, uv.VoteType.DOWNVOTE))
        total_index = round((country.corruption_index
                             + country.crime_index
                             + country.health
                             + country.disaster_risk) / 4, 4)
        advice = get_advice(country)
        return render_template('main/country.html',
                               **vars(country),
                               upvotes=upvotes,
                               downvotes=downvotes,
                               total_index=total_index,
                               advice=advice)
    abort(404)


@login_blueprint.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        if validate_user(username, password):
            login_user(get_user_by_name(username))
            flash(f'Logged in successfully.', 'success')
            return redirect(url_for('main.index'))
        else:
            flash('Login unsuccessful. Please check username and password.',
                  'warning')
    if form.errors:
        print(form.errors)
    return render_template('main/login.html', form=form)


@register_blueprint.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        existing_user = get_user_by_name(username)
        if existing_user is not None:
            flash(f'Username "{username}" is already taken. Please try again.', 'warning')
            return render_template('main/register.html', form=form)
        else:
            new_user = User(username=username, password=password, role='guest')
            add_user(new_user)
            flash(f'Account created for {form.username.data}!', 'success')
            return redirect(url_for('login.login'))
    if form.errors:
        print(form.errors)
    return render_template('main/register.html', form=form)


@main_blueprint.route('/logout')
@login_required
def logout():
    logout_user()
    flash(f'Logged out successfully.', 'success')
    return redirect(url_for('main.index'))


@main_blueprint.route('/upvote', methods=['GET', 'POST'])
@login_required
def upvote():
    country_name = request.form.get('country_name')
    country = get_country_by_name(country_name)
    if country:
        user = get_user_by_name(current_user.username)
        if uv.get_user_vote(user, country) == None:
            new_vote = uv.UserVote()
            new_vote.country_id = country.id
            new_vote.user_id = current_user.id
            new_vote.vote_id = uv.VoteType.UPVOTE.value
            uv.add_vote(new_vote)
            flash(f"You have upvoted {country_name.capitalize()}'s"
                  + " information.", 'success')
            return redirect("/country/%s" % country_name)
        else:
            flash(f'You have already voted for {country_name.capitalize()}.',
                  'warning')
            return redirect("/country/%s" % country_name)
    else:
        abort(404)


@main_blueprint.route('/downvote', methods=['GET', 'POST'])
@login_required
def downvote():
    country_name = request.form.get('country_name')
    country = get_country_by_name(country_name)
    if country:
        user = get_user_by_name(current_user.username)
        if uv.get_user_vote(user, country) == None:
            new_vote = uv.UserVote()
            new_vote.country_id = country.id
            new_vote.user_id = current_user.id
            new_vote.vote_id = uv.VoteType.DOWNVOTE.value
            uv.add_vote(new_vote)
            flash(f"You have downvoted {country_name.capitalize()}'s"
                  + " information.", 'success')
            return redirect("/country/%s" % country_name)
        else:
            flash(f'You have already voted for {country_name.capitalize()}.',
                  'warning')
            return redirect("/country/%s" % country_name)
    else:
        abort(404)


@main_blueprint.route('/vote/reset', methods=['GET', 'POST'])
@login_required
def reset_vote():
    country_name = request.form.get('country_name')
    print(country_name)
    country = get_country_by_name(country_name)
    if country:
        user = get_user_by_name(current_user.username)
        vote = uv.get_user_vote(user, country)
        if vote != None:
            uv.remove_vote(vote)
            flash(f"You have removed your vote for "
                  + "{country_name.capitalize()}.", 'success')
            return redirect("/country/%s" % country_name)
        else:
            flash(f'You have not voted for {country_name.capitalize()}.',
                  'warning')
            return redirect("/country/%s" % country_name)
    else:
        abort(404)
