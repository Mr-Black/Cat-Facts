import re
from urlparse import urljoin
from BeautifulSoup import BeautifulSoup, Comment
from random import randint
from flask import render_template, request, jsonify
from cat_facts import app
from cat_facts.database import db_session
from cat_facts.models import CatFact

@app.route('/')
def show_cat_facts():
    return render_template('index.html', cat_fact=get_cat_fact())

@app.route('/submit', methods=['POST'])
def submit_cat_fact():
    fact_text = request.form['fact']
    fact_text = sanitizeHtml(fact_text)
    fact_text = fact_text.strip()
    if len(fact_text) > 0:
        fact = CatFact(fact_text)
        db_session.add(fact)
        db_session.commit()
        app.config['CAT_FACTS'] += 1
        return jsonify(fact.serialize())     

@app.route('/getfact', methods=['GET'])
def get_fact():
    fact = get_cat_fact()
    return jsonify(fact.serialize())

def get_cat_fact():
    num = app.config['CAT_FACTS']
    if(num > 0):
        fact_number = randint(1, num)
    else:
        fact_number= num
    catfact = CatFact.query.filter(CatFact.id == fact_number).first()
    return catfact

def sanitizeHtml(value, base_url=None):
    rjs = r'[\s]*(&#x.{1,7})?'.join(list('javascript:'))
    rvb = r'[\s]*(&#x.{1,7})?'.join(list('vbscript:'))
    re_scripts = re.compile('(%s)|(%s)' % (rjs, rvb), re.IGNORECASE)
    validTags = ''.split()
    validAttrs = ''.split()
    urlAttrs = 'href src'.split() # Attributes which should have a URL
    soup = BeautifulSoup(value)
    for comment in soup.findAll(text=lambda text: isinstance(text, Comment)):
        # Get rid of comments
        comment.extract()
    for tag in soup.findAll(True):
        if tag.name not in validTags:
            tag.hidden = True
        attrs = tag.attrs
        tag.attrs = []
        for attr, val in attrs:
            if attr in validAttrs:
                val = re_scripts.sub('', val) # Remove scripts (vbs & js)
                if attr in urlAttrs:
                    val = urljoin(base_url, val) # Calculate the absolute url
                tag.attrs.append((attr, val))

    return soup.renderContents().decode('utf8')
