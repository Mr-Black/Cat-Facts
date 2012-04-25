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
    fact = CatFact(request.form['fact'])
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
