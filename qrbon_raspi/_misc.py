#!/usr/bin/env python
# -*- coding: utf-8 -*-
import Tkinter as tk

import requests

from _checkout_api import CheckoutApi
from _qr_maker import QrMaker
from _receipt_creator import create_test_receipt


class Misc:
    """
    Class with important methods for connecting the parts of qrbon.
    Puts graphics and logic together. Please create an instance to run it.
    """

    def __init__(self, server_url='http://www.qr-bon.com/receipt'):
        """Runs class"""
        self.__SERVER_URL = server_url
        self.__CHECKOUT = CheckoutApi()
        self.__WN = tk.Tk()
        self.__asking_screen()

    def __asking_screen(self):
        """The screen between qr screens. Asks the user for a digital receipt"""
        self.__WN.attributes('-fullscreen', True)
        self.__WN.configure(background="#FFEC8B")

        tk.Label(master=self.__WN, text='Ich möchte:', font='Verdana 35 bold',
                 fg='black', bg="#FFEC8B").pack()
        tk.Button(master=self.__WN, text='     einen digitalen Kassenbon     ', font='Verdana 20 bold', fg='black',
                  bg='orange', height=self.__WN.winfo_height() / 3, command=self.__next).pack()
        tk.Button(master=self.__WN, text='einen ausgedruckten Kassenbon', font='Verdana 20 bold', fg='black',
                  bg='orange', height=self.__WN.winfo_height() / 3, command=self.__CHECKOUT.paper_receipt).pack()

        self.__WN.mainloop()

    def __send_and_receive(self):
        """
        Takes the data from the checkout, sends it to the server and receives the url for
        a random receipt page.
        :return: (str) url to receipt page
        """

        receipt = create_test_receipt()
        res = requests.post(self.__SERVER_URL, json=receipt)  # Returns response object
        return str(res.text).replace('"', '')

    def __next(self):
        """Executes the programm and prepare for the next customer"""
        self.__WN.destroy()
        url = self.__send_and_receive()
        QrMaker(url)


if __name__ == '__main__':
    Misc()
