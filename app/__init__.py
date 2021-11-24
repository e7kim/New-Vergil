# Third-party imports
from flask import Flask, g
from turbo_flask import Turbo
import os

# Application imports
from app.routes import home, instructors, classes, wishlist
from app.utils import jinja_filters
from config import Config
from db import DbManager


# Create server
app = Flask(__name__)
app.config.from_object(Config)


# Initialize DB manager
db = DbManager(db_uri=os.getenv('DATABASE_URI'), query_dir='sql', debug=False)


@app.before_request
def before_request():
    try:
        g.db = db
        g.db.open_conn()
    except Exception:
        print("uh oh, problem connecting to database")
        import traceback
        traceback.print_exc()
        g.db = None


@app.teardown_request
def teardown_request(exception):
    """
    At the end of the web request, this makes sure to close the database connection.
    If you don't, the database could run out of memory!
    """
    try:
        g.db = db.close_conn()
    except Exception:
        pass


# Register extensions
turbo = Turbo(app)

# Register routing
app.register_blueprint(home.bp)
app.register_blueprint(instructors.bp)
app.register_blueprint(classes.bp)
app.register_blueprint(wishlist.bp)

# Register custom Jinja filters
app.jinja_env.filters['hash8'] = jinja_filters.hash8
