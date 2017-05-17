"""Python Flask WebApp Auth0 integration example (without JS)."""

from functools import wraps

from auth0.v3.authentication import Database, Users
from auth0.v3.exceptions import Auth0Error
from flask import Flask
from flask import redirect
from flask import render_template
from flask import session

import config
from config import AUTH0_CLIENT_ID, AUTH0_CONNECTION, AUTH0_DOMAIN, SESSION_PROFILE_KEY
from forms import LoginForm

APP = Flask(__name__)
APP.config.from_object(config)

auth0_db = Database(AUTH0_DOMAIN)
auth0_users = Users(AUTH0_DOMAIN)


def requires_auth(f):
    """Decorator to check whether the user is logged in. Redirect to login page if not."""

    @wraps(f)
    def wrapper(*args, **kwargs):
        if SESSION_PROFILE_KEY not in session:
            return redirect('/login')
        return f(*args, **kwargs)

    return wrapper


@APP.route('/')
def home():
    return render_template('home.html')


@APP.route('/dashboard')
@requires_auth
def dashboard():
    return render_template('dashboard.html',
                           user=session[SESSION_PROFILE_KEY])


@APP.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()

    if not form.is_submitted():
        return render_template('login.html', form=form)

    if not form.validate():
        return render_template('login.html', form=form), 400

    try:
        tokens = auth0_db.login(client_id=AUTH0_CLIENT_ID,
                                connection=AUTH0_CONNECTION,
                                username=form.username.data,
                                password=form.password.data)
    except Auth0Error as err:
        form.username.errors = [err.message]
        form.password.errors = [err.message]
        return render_template('login.html', form=form), 400

    profile = auth0_users.tokeninfo(tokens['id_token'])
    session[SESSION_PROFILE_KEY] = profile

    return redirect('/dashboard')


if __name__ == "__main__":
    APP.run(host='0.0.0.0', port=config.SERVER_PORT)
