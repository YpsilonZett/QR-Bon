#!/usr/bin/env python
# -*- coding: utf-8 -*-
import random
from datetime import datetime

__CHOOSE_FROM = [
    '200g Äpfel',
    '200g Birnen',
    '1kg Kartoffeln',
    'Schweinesteak',
    'Oliven',
    'Lachs Filet',
    'Frische Brötchen',
    'Himbeertorte',
    'Milka Schokolade',
    '6er Pack Quellwasser',
    '6 Bio Eier aus Bodenlandhaltung',
]


def create_test_receipt():
    receipt = {
        'store_header': "REWE<br>Ostseestraße 23<br>013088 Berlin<br>Tel.: 030 40043300",
        'store_footer': "Vielen Dank für ihren Einkauf<br>Wünscht ihnen REWE GMBH<br>"
                        "Bitte besuchen Sie uns bald wieder<br>Öffnungszeiten:<br>Mo-Sa 07:00-22:00<br><br>"
                        "Steuer. Nr.: 215/5940/2801",
        'servant': 'Herr Tester',
        'cert': '64657916279037954902029461978787888427589320574025497'
    }
    random.shuffle(__CHOOSE_FROM)
    items = __CHOOSE_FROM[:random.randint(3, 9)]  # TODO: More items
    items_info = [('{:.2f}'.format(round(random.uniform(0.0, 10.0), 2)), random.choice(['A', 'B']))
                  for _ in range(len(items))]
    receipt['sum'] = sum([float(el[0]) for el in items_info])
    receipt['items'] = dict(zip(items, items_info))
    receipt['money'] = [100, 100 - float(receipt['sum'])]
    receipt['datetime'] = datetime.now().strftime("%d.%m.%Y %H:%M").split()
    receipt['receipt_num'] = random.randint(100, 1000)
    receipt['store_num'] = random.randint(1000, 10000)
    receipt['checkout_num'] = random.randint(1, 9)
    receipt['bed'] = random.randint(100000, 1000000)
    receipt['points'] = random.randint(0, 10)
    receipt['tax_percentage'] = {'a': 19.0, 'b': 7.0}
    receipt['brutto'] = {'a': round(sum([float(v[0]) for k, v in receipt['items'].items() if v[1] == 'A'])),
                         'b': round(sum([float(v[0]) for k, v in receipt['items'].items() if v[1] == 'B']))}
    receipt['tax'] = {
        'a': round(receipt['brutto']['a'] / (100 + receipt['tax_percentage']['a']) * receipt['tax_percentage']['a'], 2),
        'b': round(receipt['brutto']['b'] / (100 + receipt['tax_percentage']['b']) * receipt['tax_percentage']['b'], 2)}
    receipt['netto'] = {'a': round(receipt['brutto']['a'] - receipt['tax']['a'], 2),
                        'b': round(receipt['brutto']['b'] - receipt['tax']['b'], 2)}
    return receipt


if __name__ == '__main__':
    print create_test_receipt()
