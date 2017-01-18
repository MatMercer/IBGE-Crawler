import bleach

from ibge_crawler.webscraper import WebScraper


class MunScraper(WebScraper):
    def __init__(self, html: str):
        html = bleach.clean(html, tags=["td"], attributes=["class"])
        super().__init__(html)
