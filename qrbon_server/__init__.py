#!/usr/bin/env python
# -*- coding: utf-8 -*-
from os import urandom

from ._views import *

# TODO: exception handling
# TODO: Frontend
# TODO: foreignkey
# TODO: receipt tests


# initializing flask
app = flask.Flask(__name__)
app.secret_key = urandom(32)  # 32 byte random string

# add pages (bind view functions to urls)
app.add_url_rule('/', view_func=home_page)
app.add_url_rule('/register', view_func=register_page, methods=["GET", "POST"])
app.add_url_rule('/login', view_func=_views.login_page, methods=["GET", "POST"])
app.add_url_rule('/dashboard', view_func=dashboard_page)
app.add_url_rule('/logout/', view_func=logout_page)
app.add_url_rule('/receipt', view_func=receipt_request_page, methods=["POST"])
app.add_url_rule('/rid=<string:rid>', view_func=temp_url_page)

# @app.before_request
# def log_request():
#     """
#     Logs all requests instead of werkzeug request logger, because it isn't working.
#     Example: "GET" http://www.qr-bon.com/ (127.0.0.1) - ImmutableDict() | {"Test": "Json"}
#     """
#
#     logging.debug('<REQUEST-HANDLER> "{method}" {url} ({ip}) - {content} | {json}'.format(
#         method=flask.request.method,
#         url=flask.request.url,
#         ip=flask.request.remote_addr,
#         content=flask.request.form,
#         json=flask.request.json
#     ))


if __name__ == '__main__':
    app.run(debug=True)
