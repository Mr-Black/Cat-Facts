from sqlalchemy import Column, Integer, UnicodeText
from cat_facts.database import Base

class CatFact(Base):
    __tablename__ = 'catfacts'
    id = Column(Integer, primary_key=True)
    factoid = Column(UnicodeText())

    def __init__(self, factoid=None):
        self.factoid = factoid

    def __repr__(self):
        return '<CatFact: %d: %r>' % (self.id, self.factoid)
    
    def serialize(self):
        return {
            'id' : self.id,
            'factoid': self.factoid,
        }
