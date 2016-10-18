#!/usr/bin/env python
# -*- coding: utf-8 -*-
import logging
from os import urandom

import flask

import _views

# TODO: better logging
# TODO: exception handling
# TODO: Frontend
# TODO: foreignkey assoziation

#logging.basicConfig(level=logging.DEBUG)

# initializing flask
app = flask.Flask(__name__)
app.secret_key = urandom(32)  # 32 byte random string

# add pages (bind view functions to urls)
app.add_url_rule('/', view_func=_views.home_page)
app.add_url_rule('/register', view_func=_views.register_page, methods=["GET", "POST"])
app.add_url_rule('/login', view_func=_views.login_page, methods=["GET", "POST"])
app.add_url_rule('/dashboard', view_func=_views.dashboard_page)
app.add_url_rule('/logout', view_func=_views.logout_page)
app.add_url_rule('/receipt', view_func=_views.receipt_request_page, methods=["POST"])
app.add_url_rule('/rid=<string:rid>', view_func=_views.temp_url_page)


@app.before_request
def log_request():
    logging.debug(flask.request.method + ' request to ' + flask.request.url + ' from ' +
                  flask.request.remote_addr + ', content: ' + str(flask.request.form))


if __name__ == '__main__':
    app.run(debug=True)
