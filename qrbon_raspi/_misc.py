#!/usr/bin/env python
# -*- coding: utf-8 -*-
import Tkinter as tk
import requests

from ._receipt_creator import create_test_receipt
from ._qr_maker import QrMaker


class Misc:
    """
    Class with important methods for connecting the parts of qrbon.
    Puts graphics and logic together. Please create an instance to run it.
    """

    def __init__(self, server_url='http://www.qr-bon.com/receipt'):
        """Runs class"""
        self.__SERVER_URL = server_url
        self.__WN = tk.Tk()
        self.__asking_screen()

    def __asking_screen(self):
        """The screen between qr screens. Asks the user for a digital receipt"""
        self.__WN.attributes('-fullscreen', True)
        self.__WN.configure(background="#FFEC8B")

        tk.Label(master=self.__WN, text='Möchten Sie\neinen\ndigitalen\nKassenbon?', font='Verdana 37 bold',
            fg='black', bg="#FFEC8B").pack()

        tk.Button(master=self.__WN, text='  JA!  ', font='Verdana 46 bold', fg='black',
            bg='orange', command=self.__next).pack()

        self.__WN.mainloop()

    def __send_and_receive(self):
        """
        Takes the data from the checkout, sends it to the server and receives the url for
        a random receipt page.
        :return: (str) url to receipt page
        """

        print 'Lade...'
        receipt = create_test_receipt()
        res = requests.post(self.__SERVER_URL, json=receipt)  # Returns response object
        return res.text

    def __next(self):
        """Executes the programm and prepare for the next customer"""
        self.__WN.destroy()
        url = self.__send_and_receive()
        QrMaker(url)
