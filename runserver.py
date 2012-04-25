from cat_facts import app
from cat_facts.models import CatFact
"""
    This should only occur on startup. I will
    eventually change the database so that I can
    just sort the rows in a random worder but
    SQLite doesn't support that so for the time
    being I'm just going to cache the total number of
    rows.
"""
app.config['CAT_FACTS'] = CatFact.query.count()
app.run(debug=True)
