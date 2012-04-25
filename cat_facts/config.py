from sqlalchemy.ext.declarative import declarative_base

DATABASE = 'sqlite:///cat_facts.db'
BASE = declarative_base()
DEBUG = True
SECRET_KEY = 'development key'
CAT_FACTS = 0
