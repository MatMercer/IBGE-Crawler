from ibge_crawler.common import ibge_logger, utf8_request
from csv import writer, reader

from ibge_crawler.mun_info_scraper import MunInfoScraper
from ibge_crawler.mun_scraper import MunScraper


def scrape_muns():
    ibge_logger.debug("Opening links.csv...")
    with open("links.csv", "r") as link_csv:
        link_reader = reader(link_csv)
        ibge_logger.debug("Opening municipios.csv...")
        with open("municipios.csv", "w") as mun_csv:
            mun_writer = writer(mun_csv)

            mun_total = 0
            for row in link_reader:
                mun_total += 1
                ibge_logger.info("Scraping %s ~ %s..." % (row[0], row[1]))

                # Get the brief html
                brief_html = utf8_request(row[3])

                # Get the info html
                info_html = utf8_request(row[4])

                # Scrape the brief
                brief_scr = MunScraper(brief_html)
                brief = brief_scr.as_dict()

                # Scrape the info
                info_scr = MunInfoScraper(info_html)
                info = info_scr.as_dict()

                print(brief)
                print(info)

            ibge_logger.info("Scraped %d municipios to municipios.csv." % mun_total)


if __name__ == "__main__":
    scrape_muns()
