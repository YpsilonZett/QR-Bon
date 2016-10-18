#!/usr/bin/env python
# -*- coding: utf-8 -*-
import logging
from gc import collect as clean_cache

import flask

from _misc import Misc
from _users import UserHandler

user_handler = UserHandler()


def home_page():
    """Homepage of QR receipt, contains description and overview."""
    return flask.render_template('index.html')


def register_page():
    """Page for creating a new account"""
    if flask.request.method == 'POST':
        email = flask.request.form['email']
        username = flask.request.form['username']
        password = flask.request.form['password']  # TODO: Password hash, if necessary

        if user_handler.new_user(email, username, password):
            flask.session['logged_in'] = True
            flask.session['username'] = username
            logging.debug(flask.request.remote_addr + ' registered successfully as ' + username)
            return flask.redirect(flask.url_for('dashboard_page'))

        logging.debug(flask.request.remote_addr + ' tried to register unsuccessfully')
        return flask.render_template('register.html',
                                     error='Tut uns leid, aber der Name existiert beriets')

    return flask.render_template('register.html')


def login_page():
    """User login page"""

    if flask.request.method == 'POST':
        usr_name = flask.request.form['username']
        usr_pwd = flask.request.form['password']

        if user_handler.check_login(usr_name, usr_pwd):
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
                                     error='Ungültige Kombination aus Benutzername und Passwort'.decode
                                     ('utf-8'))  # TODO: Encoding

    return flask.render_template('login.html')


@Misc.login_required
def dashboard_page():
    """Profile page"""

    receipts = user_handler.receipt_overview(flask.session['username'])
    logging.debug('receipts for ' + flask.request.remote_addr + ' loaded successfully: ' + str(receipts))
    return flask.render_template('dashboard.html', receipts=receipts)


@Misc.login_required
def logout_page():
    """Redirects user to homepage and cleans session"""

    flask.session.clear()
    clean_cache()
    logging.debug(flask.request.remote_addr + ' logged out')
    return flask.redirect(flask.url_for('home_page'))


def receipt_request_page():
    """Gets POST requests from RasPis and gives the receipts to the receipt handler"""
    receipt = str(flask.request.get_json(force=True))
    logging.debug('got receipt from ' + flask.request.remote_addr + ': ' + str(receipt))
    receipt_id = user_handler.receipt_to_db(receipt)
    logging.debug('put receipt ' + receipt + ' with id ' + receipt_id + ' in database')
    url = 'http://localhost:5000/rid=' + receipt_id  # www.qr-bon.com
    logging.debug('created url for ' + flask.request.remote_addr + ' successfully: ' + url + ', sending back...')
    return flask.jsonify(url)


@Misc.login_required
def temp_url_page(rid):
    """
    Temporary page where receipts are stored. The user, which visits it first, get the receipt.
    :param rid: (str) receipt id (user is assigned to receipt with this id)
    """

    user_handler.assign_rid_user(rid, flask.session['username'])
    return flask.redirect(flask.url_for('dashboard_page'))
