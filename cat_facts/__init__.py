import config
import sqlalchemy
from flask import Flask

app = Flask(__name__)
app.config.from_object(config)

import cat_facts.views
from cat_facts.database import db_session
from cat_facts.models import CatFact


@app.teardown_request
def shutdown_session(exception=None):
    db_session.remove()
