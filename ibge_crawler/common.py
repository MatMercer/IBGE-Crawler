from urllib.request import urlopen

import logging


logging.basicConfig(level=logging.DEBUG, format="%(name)s | %(asctime)s: %(levelname)s - %(message)s", datefmt="%d/%m/%Y %H:%M:%S")
ibge_logger = logging.getLogger("IBGE CRAWLER")


def utf8_request(url: str) -> str:
    ibge_logger.debug("Requeting %s..." % url)
    response = urlopen(url)
    response_buf = response.read()
    return response_buf.decode()


