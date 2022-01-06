import logging
from scrape import Scrape
from logging.handlers import RotatingFileHandler

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
log = logging.getLogger(__name__)
handler = RotatingFileHandler('app.log', maxBytes=2000, backupCount=5)
log.addHandler(handler)


if __name__ == '__main__':
    pass

