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
                return f(*args, **kwargs)

            return flask.redirect(flask.url_for('login_page', goto=flask.request.url))

        return inner

    @staticmethod
    def test_receipt(receipt):
        """Tests, if the given receipt (str) is a real 'qr bon' and returns boolean"""
        return True

    @staticmethod
    def generate_rid():
        """
        :return: (str) random receipt id (hashed random string and timestamp)
        """

        return ''.join(SystemRandom().choice(ascii_letters + digits) for _ in range(10)) + \
               sub(r"\D", "", str(datetime.now())[4:])[4:-6]
