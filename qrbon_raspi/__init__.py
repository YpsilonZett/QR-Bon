#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
This part of QR Bon runs on a Raspberry Pi, which is connected to a checkout in the store,
where Qr Bon is used. Simply import the package and tun the main() function to start the program.
The program is running in a while loop, so it will never stop, except you shutdown the Raspberry Pi.
I don't recommend this, because the Raspberry Pi have to be handled with care. (Later on there will
be a nice way to shutdown.
"""
from ._misc import Misc


__author__ = "Yorick Zeschke"
__copyright__ = "Copyright 2016, The QR-Bon Project"
__credits__ = ["Yorick Zeschke"]
__license__ = "Apache2"
__version__ = "1.0.0"
__maintainer__ = "Yorick Zeschke"
__email__ = "yorick.zeschke@gmail.com"
__status__ = "Prototype"


def start_program():
    """PLease execute this to run the program"""
    while True:  # TODO: Change condition
        Misc()


if __name__ == '__main__':
    start_program()
