import re

from bs4 import BeautifulSoup

from ibge_crawler.dicto_closured import DictClosured


class WebScraper(DictClosured):
    def __init__(self, html: str, clean_html: bool=True):
        if clean_html:
            html = self._clean_html(html)
        self._soup = BeautifulSoup(html, "lxml")

    @staticmethod
    def _clean_html(html: str):
        html = html.replace("&nbsp;", " ")

        # Remove formating and double spaces
        html = re.sub(r"(\n|\t| {2,})", "", html)

        # Remove trailing spaces close to dom elements
        html = re.sub(r">\s", ">", html)
        html = re.sub(r"\s<", "<", html)

        # Remove empty elements
        html = re.sub(r"<(\w+)></\1>", "", html)
        return html
