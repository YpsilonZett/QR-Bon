#!/usr/bin/env python
# -*- coding: utf-8 -*-
import Tkinter as tk

import qrcode
from PIL import ImageTk


class QrMaker:
    """
    Class to create qr codes, save them as picture
    and display them after that. It's an independent class, so you just need to
    initialize an instance to run it.
    """

    def __init__(self, url, qr_size=1, pattern_size=6, border_size=3,
                 error_correction_level=qrcode.constants.ERROR_CORRECT_H):
        """
        Setting up everything
        :param url: (str) Url inside the code
        :param server_connection: (obj) function call of 'ServerCommunication(...).code_scanned()'
        :param qr_size: Size of qr code
        :param pattern_size: Size of one qr pixel
        :param border_size: Thickness of border
        :param error_correction_level: Intensity of alert correction
        """

        self.__URL = url
        self.__SIZE = qr_size
        self.__BOX = pattern_size
        self.__BD = border_size
        self.__ERR = error_correction_level
        self.__init_graphics()

    def __init_graphics(self):
        """Initializes al graphics and starts the qr-screen"""
        self.__STATE = True
        self.__WN = tk.Tk()
        self.__WN.update()
        self.__QR_IMG = self.__generate_qr()
        self.__BG_COL = "#FFEC8B"
        self.__SCREEN_WIDTH, self.__SCREEN_HEIGHT = 480, 320

        # Init window
        self.__WN.configure(background=self.__BG_COL)
        self.__WN.attributes('-fullscreen', True)
        self.__qr_screen()
        self.__WN.mainloop()

    def __generate_qr(self):
        """
        Uses module qrcode the generate qr img object
        :return: (obj) image
        """

        qr = qrcode.QRCode(version=self.__SIZE, error_correction=self.__ERR,
                           box_size=self.__BOX, border=self.__BD)
        qr.add_data(self.__URL)
        qr.make(fit=True)
        return qr.make_image()

    def __qr_screen(self):
        """Creates a canvas object displayed on the screen. It contains the qr image."""
        self.__QR_IMG = self.__QR_IMG.resize((self.__SCREEN_HEIGHT, self.__SCREEN_HEIGHT))
        self.__QR_IMG = ImageTk.PhotoImage(self.__QR_IMG)
        tk.Label(master=self.__WN, image=self.__QR_IMG).place(x=0, y=0)

        tk.Label(master=self.__WN, text='Bitte\nQR\nCode\nscannen',
            font='Verdana 23 bold', fg='black', bg=self.__BG_COL).\
            place(x=self.__SCREEN_HEIGHT + 7, y=22)

        tk.Button(master=self.__WN, text='\n  Fertig  \n', font='Verdana 20 bold',
            fg='black', bg='orange', bd=1, command=self.__WN.destroy). \
            place(x=self.__SCREEN_HEIGHT, y=self.__SCREEN_HEIGHT - 109)
