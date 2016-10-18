import logging

# sys.path.insert(0, '/var/www/Server')

logging.basicConfig(level=logging.DEBUG,
                    format='[%(asctime)s] %(levelname)s: %(message)s',
                    datefmt='%d/%m/%Y %I:%M:%S %p',
                    filename='qrbon_server/logs/debug.log',
                    filemode='a')

from qrbon_server import app as application

logging.info("\n\n----- Starting QR Bon -----\n\n")
application.run()
