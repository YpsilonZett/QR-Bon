#!/usr/bin/env python
# -*- coding: utf-8 -*-
import logging
from datetime import datetime
from functools import wraps
from random import SystemRandom
from string import ascii_letters, digits

import flask


class Misc(object):
    """Helper functions for miscellaneous things"""

    @staticmethod
    def login_required(f):
        """Decorator for pages, which require a login"""

        @wraps(f)
        def inner(*args, **kwargs):
            if 'logged_in' in flask.session:
                logging.debug("<MISC> {ip} (logged in) ACCESS GRANTED: {url}".
                              format(ip=flask.request.remote_addr, url=flask.request.url))
                return f(*args, **kwargs)

            logging.debug("<MISC> {ip} (not logged in) ACCESS DENIED: {url} -> redirect to login".
                          format(ip=flask.request.remote_addr, url=flask.request.url))
            return flask.redirect(flask.url_for('login_page', goto=flask.request.url))

        return inner

    @staticmethod
    def test_receipt(receipt):
        """Tests, if the given receipt (dict) is a real 'qr bon' and returns boolean"""
        if receipt['cert'] == '64657916279037954902029461978787888427589320574025497':
            logging.info("<MISC> Receipt tested - TRUE ({receipt})".format(receipt=receipt))
            return True

        return False

    @staticmethod
    def generate_rid():
        """
        :return: (str) random receipt id (hashed random string and timestamp)
        """

        rid = ''.join(SystemRandom().choice(ascii_letters + digits) for _ in range(12)) + \
              "{:%d%m%H%M%S}".format(datetime.now())
        logging.debug("<MISC> Created rid: {rid}".format(rid=rid))
        return rid

    @staticmethod
    def alert_html(msg, kind):
        """
        Creates html for a bootstrap alert div, which can be given as argument at template rendering
        :param msg: (str) message, which is put into the alert
        :param kind: (str) ['success'|'info'|'warning'|'danger'] alert kiind
        :return: (str) html for an alert div
        """

        return u'<div class="alert alert-{kind}" style="margin-top: 10px; font-size: x-large">{msg}</div>'. \
            format(kind=kind, msg=msg)
