#!/usr/bin/env python
# -*- coding: utf-8 -*- b
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
        password2 = flask.request.form['password2']

        if password != password2:
            return flask.render_template('register.html',
                                         alert=Misc.alert_html(u'Die Angegebenen Passwörter stimmen nicht überein',
                                                               'danger'))

        if user_handler.new_user(email, username, password):
            flask.session['logged_in'] = True
            flask.session['username'] = username
            logging.debug(flask.request.remote_addr + ' registered successfully as ' + username)
            return flask.redirect(flask.url_for('dashboard_page'))

        logging.debug(flask.request.remote_addr + ' tried to register unsuccessfully')
        return flask.render_template('register.html', alert=Misc.alert_html(
            'Der Benutzername ist bereits vergeben', 'danger'
        ))

    return flask.render_template('register.html', alert='')


def login_page():
    """User login page"""

    if flask.request.method == 'POST':
        usr_name = flask.request.form['username']
        usr_pwd = flask.request.form['password']

        if user_handler.check_login(usr_name, usr_pwd):
            flask.session['logged_in'] = True
            flask.session['username'] = usr_name
            clean_cache()
            logging.debug(flask.request.remote_addr + ' logged in successfully as ' + usr_name)
            if flask.request.args.get('goto', '') == '':
                return flask.redirect(flask.url_for('dashboard_page'))

            return flask.redirect(flask.request.args.get('goto', ''))

        clean_cache()
        logging.debug(flask.request.remote_addr + ' tried to log in unsuccessfully')
        return flask.render_template('login.html', alert=Misc.alert_html(
            u'Ungültige Kombination aus Benutzername und Passwort', 'danger'
        ))

    return flask.render_template('login.html', alert='')


@Misc.login_required
def dashboard_page():
    """Profile page"""

    receipts = user_handler.receipt_overview(flask.session['username'])
    logging.debug("<DASHBOARD> Receipts for {ip} loaded successful ({num} receipts)".
                  format(ip=flask.request.remote_addr, num=len(receipts)))
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
    receipt = flask.request.get_json(force=True)
    logging.info('got receipt from ' + flask.request.remote_addr)
    if not Misc.test_receipt(receipt):
        logging.warn("<MISC> Bad receipt! {ip} send bad receipt, cancelling request! Bad receipt: {receipt}".format(
            ip=flask.request.remote_addr, receipt=receipt))
        flask.abort(400)
        return

    receipt_id = user_handler.receipt_to_db(str(receipt))
    url = 'http://www.qr-bon.com/rid=' + receipt_id  #
    logging.debug('created url for ' + flask.request.remote_addr + ' successfully: ' + url + ', sending back...')
    return flask.jsonify(url)


@Misc.login_required
def temp_url_page(rid):
    """
    Temporary page where receipts are stored. The user, which visits it first, get the receipt.
    :param rid: (str) receipt id (user is assigned to receipt with this id)
    """

    if not user_handler.assign_rid_user(rid, flask.session['username']):
        logging.warn('Trying to steal receipt! {ip} has visited page: {url}! Cancelling request!'.
                     format(ip=flask.request.remote_addr, url=flask.request.url))
        flask.abort(400)
        return

    return flask.redirect(flask.url_for('dashboard_page'))
