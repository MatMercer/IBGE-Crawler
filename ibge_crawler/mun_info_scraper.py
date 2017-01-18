import bleach
import re

from ibge_crawler.mun_scraper import MunScraper
from ibge_crawler.webscraper import WebScraper


class MunInfoScraper(WebScraper):
    def _data_by_alike_text(self, name: str):
        alike_regex = re.compile("^%s.*" % name)

        label = self._soup.find(text=alike_regex).parent
        data_el = label.next_sibling

        return data_el.text

    def pib(self):
        data = self._data_by_alike_text("PIB per capita")

        return self._float_data(data)
