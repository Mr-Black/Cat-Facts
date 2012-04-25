import config
import sqlalchemy
from flask import Flask

app = Flask(__name__)
app.config.from_object(config)

import cat_facts.views
from cat_facts.database import db_session
from cat_facts.models import CatFact

"""
    This should only occur on startup and when
    a new fact is added to the database. I will
    eventually change the database so that I can
    just sort the rows in a random worder but
    SQLite doesn't support that so for the time
    being I'm just going to cache the total number of
    rows.
"""
app.config['CAT_FACTS'] = CatFact.query.count()

@app.teardown_request
def shutdown_session(exception=None):
    db_session.remove()
