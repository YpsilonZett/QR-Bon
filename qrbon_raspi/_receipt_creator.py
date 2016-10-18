#!/usr/bin/env python
# -*- coding: utf-8 -*-
import datetime
import random


__STANDARD_ITEMS = [
    'Raspberry Pi',
    'Python Buch für Profis',
    'Arduino Pro Micro Kit',
    'Nerd Kartenspiel',
    '50 Inch Monitor',
    '1200 DPI Gaming Mouse',
    'Alpaka'
]


def __general_info():
    """
    Creates general information
    :returns tuple: (datetime, store)
    """

    store = ('Test Laden', 'Teststraße 0', 13088, 'Berlin')  # TODO: Change to Rewe
    return datetime.datetime.now().strftime("%Y.%m.%d %H:%M:%S"), store


def __random_items(item_list):
    """
    Some of the given items as random list
    :param item_list: (list) min length = 5
    :returns tuple: (item{name: ..., price: ..., ean: ....}, ...)
    """

    random.shuffle(item_list)
    items = []
    for item in item_list[:4]:
        items.append({
            'name': item,
            'price': random.randrange(0, 1000),
            'ean': random.randint(10000000000, 99999999999)
        })

    return tuple(items)


def __receipt_structure(item_list):
    """
    Creates a receipt object
    :param item_list:
    :returns dict: a receipt
    """

    receipt = {}
    inf = __general_info()
    receipt['datetime'] = inf[0]
    receipt['store'] = inf[1]
    receipt['items'] = __random_items(item_list)
    return receipt


def create_test_receipt():
    return __receipt_structure(__STANDARD_ITEMS)


if __name__ == '__main__':
    print create_test_receipt()
