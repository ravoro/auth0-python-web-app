from os import environ as env, path

from dotenv import load_dotenv

load_dotenv(path.join(path.dirname(__file__), '.env'))

# Flask app-related config
DEBUG = True
SECRET_KEY = env['APP_SECRET_KEY']
SERVER_PORT = 3000
SESSION_PROFILE_KEY = 'profile'

# Auth0-related config
AUTH0_CLIENT_ID = env['AUTH0_CLIENT_ID']
AUTH0_CLIENT_SECRET = env['AUTH0_CLIENT_SECRET']
AUTH0_CONNECTION = env['AUTH0_CONNECTION']
AUTH0_DOMAIN = env['AUTH0_DOMAIN']
