#!/usr/bin/env python
# -*- coding: utf-8 -*-
from functools import wraps
from string import ascii_letters, digits
from random import SystemRandom
from gc import collect as clean_cache
from os import urandom
import logging

import flask
import MySQLdb


app = flask.Flask(__name__)
app.secret_key = urandom(32)  # 32 byte random string
logging.basicConfig(level=logging.DEBUG)


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

    # @staticmethod
    # @app.before_request
    # def log_request():
    #     logging.debug(flask.request.method + ' request to ' + flask.request.url + ' from ' +
    #                   flask.request.remote_addr + ', content: ' + str(flask.request.form))


class UserHandler(object):
    """
    Class with functions for user management. Has SQL interface.
    Note: No exception handling in this class.
    """

    def __init__(self):
        self.__CURSOR, self.__CONNECTION = self.__db_connect()

    def __db_connect(self):
        """
        Connects to the database.
        :return: (tuple): ((obj) database cursor, (obj) database connection)
        """

        conn = MySQLdb.connect(host="localhost",
                               user="root",
                               passwd="Alay22xmp",
                               db="qrbon")
        c = conn.cursor()
        return c, conn

    def new_user(self, email, username, password):
        """
        Creates a new user in the database
        :param email: (string) email address, typed into register form
        :param username: (string) username, typed into register form
        :param password: (string) password, typed into register form
        :return: (bool) True, if success or False, if user exists
        """

        status_code = self.__CURSOR.execute(
            "SELECT * FROM users WHERE username = ('{usr_name}')".
            format(usr_name=MySQLdb.escape_string(username))
        )
        if int(status_code) > 0:  # Means, that SQL has found an user with this name
            return False

        self.__CURSOR.execute(
            "INSERT INTO users (username, password, email) VALUES ('{name}', '{pwd}', '{email}')".
            format(name=MySQLdb.escape_string(username),
                   pwd=MySQLdb.escape_string(password),
                   email=MySQLdb.escape_string(email))
        )
        self.__CONNECTION.commit()
        return True

    def check_login(self, username, password):
        """
        Checks, whether the given password is the real user password.
        :param username: (str) name of the user
        :param password: (str) given password to check
        :return: (bool) True, if login is ok, False, if not
        """

        self.__CURSOR.execute(
            "SELECT password FROM users WHERE username = ('{usr_name}')".
            format(usr_name=MySQLdb.escape_string(username))
        )
        real_password = self.__CURSOR.fetchone()

        if real_password is not None:
            if real_password[0] == password:
                return True

        return False

    def __get_user_id(self, username):
        """
        Gets the unique foreignkey for a user from the database
        :param username: (str) name of the user
        :return: (int) primary key of the user
        """

        self.__CURSOR.execute(
            "SELECT uid FROM users WHERE username = ('{user_name}')".
            format(user_name=MySQLdb.escape_string(username))
        )
        return int(self.__CURSOR.fetchone()[0])

    def receipt_to_db(self, receipt):
        """
        Puts a receipt with random generated id in the database, note: isn't assigned to user yet
        :param receipt: (str) string version of dictionary
        :return: (str) 16-digit id
        """

        rand_id = ''.join(SystemRandom().choice(ascii_letters + digits) for _ in range(16))
        self.__CURSOR.execute(
            "INSERT INTO receipts (receipt, receipt_id) VALUES ('{r}', '{rid}')"
            .format(r=MySQLdb.escape_string(receipt), rid=MySQLdb.escape_string(rand_id))
        )
        self.__CONNECTION.commit()
        return rand_id

    def assign_rid_user(self, rid, username):
        """
        Assigns a receipt id (from an existing receipt in the database) to an owner
        :return: (bool) True, if anything ok, else raise error
        """
        user_id = self.__get_user_id(username)
        self.__CURSOR.execute(
            "UPDATE receipts SET user_id={uid} WHERE receipt_id='{rid}'".
            format(uid=user_id, rid=rid)
        )
        self.__CONNECTION.commit()
        return True

    def receipt_overview(self, username):
        """
        Gets all receipts for the dashboard
        :param username: (str) name of the users who gets the overview
        :return: (list) raw receipt data. Needs to be formatted in the html file
        """

        self.__CURSOR.execute(
            "SELECT receipt FROM receipts WHERE user_id = ({uid})".
            format(uid=self.__get_user_id(username))
        )
        return self.__CURSOR.fetchall()


# TODO: Instance methods with 'self'
# TODO: Userhandler instance variable
# TODO: better logging
# TODO: exception handling
# TODO: Frontend
# TODO: receipt id = timestamp + random (hashed)
# TODO: foreignkey assoziation
class Views(object):
    """
    Class for page functions (rendering + logic).
    Made for better structure
    """

    @staticmethod
    @app.route('/')
    def home_page():
        """Homepage of QR receipt, contains description and overview."""
        return flask.render_template('index.html')

    @staticmethod
    @app.route('/register', methods=['GET', 'POST'])
    def register_page():
        """Page for creating a new account"""
        if flask.request.method == 'POST':
            u = UserHandler()
            email = flask.request.form['email']
            username = flask.request.form['username']
            password = flask.request.form['password']  # TODO: Password hash, if necessary

            if u.new_user(email, username, password):
                flask.session['logged_in'] = True
                flask.session['username'] = username
                logging.debug(flask.request.remote_addr + ' registered successfully as ' + username)
                return flask.redirect(flask.url_for('dashboard_page'))

            logging.debug(flask.request.remote_addr + ' tried to register unsuccessfully')
            return flask.render_template('register.html',
                                         error='Tut uns leid, aber der Name existiert beriets')

        return flask.render_template('register.html')

    @staticmethod
    @app.route('/login', methods=['GET', 'POST'])
    def login_page():
        """User login page"""

        if flask.request.method == 'POST':
            u = UserHandler()
            usr_name = flask.request.form['username']
            usr_pwd = flask.request.form['password']

            if u.check_login(usr_name, usr_pwd):
                flask.session['logged_in'] = True
                flask.session['username'] = usr_name
                clean_cache()
                logging.debug(flask.request.remote_addr + ' logged in successfully')
                if flask.request.args.get('goto', '') == '':
                    return flask.redirect(flask.url_for('dashboard_page'))

                return flask.redirect(flask.request.args.get('goto', ''))

            clean_cache()
            logging.debug(flask.request.remote_addr + ' tried to log in unsuccessfully')
            return flask.render_template('login.html',
                error='Ungültige Kombination aus Benutzername und Passwort'.decode('utf-8'))  # TODO: Encoding

        return flask.render_template('login.html')

    @staticmethod
    @app.route('/dashboard')
    @Misc.login_required
    def dashboard_page():
        """Profile page"""

        receipts = UserHandler().receipt_overview(flask.session['username'])
        logging.debug('receipts for ' + flask.request.remote_addr + ' loaded successfully: ' + str(receipts))
        return flask.render_template('dashboard.html', receipts=receipts)

    @staticmethod
    @app.route('/logout')
    @Misc.login_required
    def logout_page():
        """Redirects user to homepage and cleans session"""

        flask.session.clear()
        clean_cache()
        logging.debug(flask.request.remote_addr + ' logged out')
        return flask.redirect(flask.url_for('home_page'))

    @staticmethod
    @app.route('/receipt', methods=['POST'])
    def receipt_request_page():
        """Gets POST requests from RasPis and gives the receipts to the receipt handler"""
        receipt = str(flask.request.get_json(force=True))
        logging.debug('got receipt from ' + flask.request.remote_addr + ': '+ str(receipt))
        receipt_id = UserHandler().receipt_to_db(receipt)
        logging.debug('put receipt ' + receipt + ' with id ' + receipt_id + ' in database')
        url = 'http://localhost:5000/rid=' + receipt_id
        logging.debug('created url for ' + flask.request.remote_addr + ' successfully: ' + url + ', sending back...')
        return flask.jsonify(url)

    @staticmethod
    @app.route('/rid=<string:rid>')
    @Misc.login_required
    def temp_url_page(rid):
        """
        Temporary page where receipts are stored. The user, which visits it first, get the receipt.
        :param rid: (str) receipt id (user is assigned to receipt with this id)
        """

        print 'temp_url_page'
        UserHandler().assign_rid_user(rid, flask.session['username'])
        return flask.redirect(flask.url_for('dashboard_page'))


if __name__ == '__main__':
    app.run(debug=True)
