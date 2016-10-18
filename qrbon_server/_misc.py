import logging
from datetime import datetime
from functools import wraps
from random import SystemRandom
from re import sub
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
                logging.debug("<MISC> {ip} (not logged in) ACCESS DENIED: {url} -> redirect to login".
                              format(ip=flask.request.remote_addr, url=flask.request.url))
                return f(*args, **kwargs)

            logging.debug("<MISC> {ip} (logged in) ACCESS GRANTED: {url}".
                          format(ip=flask.request.remote_addr, url=flask.request.url))
            return flask.redirect(flask.url_for('login_page', goto=flask.request.url))

        return inner

    @staticmethod
    def test_receipt(receipt):
        """Tests, if the given receipt (str) is a real 'qr bon' and returns boolean"""
        if receipt['meta'] == 'QRBON-TRUE-RECEIPT':
            logging.debug("<MISC> Receipt tested - TRUE ({receipt})".format(receipt=receipt))
            return True

        logging.warn("<MISC> Bad receipt! {ip} send bad receipt: {receipt}".format(
            ip=flask.request.remote_addr, receipt=receipt))
        return False

    @staticmethod
    def generate_rid():
        """
        :return: (str) random receipt id (hashed random string and timestamp)
        """

        rid = ''.join(SystemRandom().choice(ascii_letters + digits) for _ in range(10)) + \
              sub(r"\D", "", str(datetime.now())[4:])[4:-6]
        logging.debug("<MISC> Created rid: {rid}".format(rid=rid))
        return rid
