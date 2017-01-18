import bleach
import re

from ibge_crawler.webscraper import WebScraper


class MunScraper(WebScraper):
    def __init__(self, html: str):
        html = bleach.clean(html, tags=["html", "body", "table", "td"], attributes=["class"], strip=True)
        super().__init__(html)

    def _data_by_alike_text(self, name: str):
        alike_regex = re.compile("^%s.*" % name)

        label = self._soup.find(text=alike_regex).parent
        data_el = label.next_sibling

        return data_el.text

    def pop_estimada(self):
        data = self._data_by_alike_text("População estimada").replace(".", "")

        return int(data)
