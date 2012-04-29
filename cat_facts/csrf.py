# from http://flask.pocoo.org/snippets/3/

# Exemption support loosely based on flask-csrf, Copyright 2010 Steve Losh and
# available under the MIT license.
# http://sjl.bitbucket.org/flask-csrf/

import base64
import os
from flask import abort, g, request, session
from werkzeug.routing import NotFound
from cat_facts import app

_exempt_views = []


def csrf_exempt(view):
    _exempt_views.append(view)
    return view


@app.before_request
def csrf_protect():
    try:
        if app.view_functions.get(request.endpoint) in _exempt_views:
            return
    except NotFound:
        pass

    if request.method in ("DELETE", "POST", "PUT"):
        token = session.pop('_csrf_token', None)
        # flask does not support data in DELETE requests,
        # so check URL parameters as well
        sent_token = request.form.get('_csrf_token')\
                or request.args.get('_csrf_token')
        if not token or token != sent_token:
            abort(400)


def some_random_string():
    return base64.urlsafe_b64encode(os.urandom(32))


def generate_csrf_token():
    if '_csrf_token' not in session:
        session['_csrf_token'] = some_random_string()
    return session['_csrf_token']

app.jinja_env.globals['csrf_token'] = generate_csrf_token
