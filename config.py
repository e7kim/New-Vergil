"""
Flask config
https://flask.palletsprojects.com/en/2.0.x/config/#development-production
"""
import os
from dotenv import load_dotenv

load_dotenv()
basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    SECRET_KEY = os.getenv('SECRET_KEY')
