from pathlib import Path

from ibge_crawler.common import ibge_logger, utf8_request
from csv import writer, reader

from ibge_crawler.mun_info_scraper import MunInfoScraper
from ibge_crawler.mun_scraper import MunScraper

convert_table = {
    ord("Á"): "A",
    ord("É"): "E",
    ord("Í"): "I",
    ord("Ó"): "O"
}


def insistent_request(url: str, limit = 10):
    if limit > 0:
        try:
            return utf8_request(url)
        except:
            ibge_logger.warn("Failed to request %s. Trying again..." % url)
            return insistent_request(url, limit - 1)
    else:
        raise Exception("Tried a request too many times.")


def clean_mun_name(name: str):
    # Convert utf-8 chars to ascii corretly
    name = name.translate(convert_table)
    name = name.upper()

    buf = name.encode("ascii", "replace")
    return buf.decode("ascii").upper()


def scrape_muns():
    ibge_logger.debug("Opening links.csv...")
    with open("links.csv", "r") as link_csv:
        link_reader = reader(link_csv)
        ibge_logger.debug("Opening municipios.csv...")

        start_index = input("What is the index you want to start from?")
        try:
            start_index = int(start_index)
            if start_index < 0:
                start_index = 0
        except ValueError:
            start_index = 0

        # Get the total
        muns_total = len(open("links.csv", "r").readlines()) - start_index
        ibge_logger.info("Going to scrape %d municipios." % muns_total)
        scraped_muns = 0

        if Path("municipios.csv").is_file():
            print("File municipios.csv already exists! Do you REALLY want to recreate it? (y)/(any for no)")
            if not input("Answer: ") == "y":
                print("Exiting... Please backup municipios.csv.")
                exit(1)

        with open("municipios.csv", "w") as mun_csv:
            mun_writer = writer(mun_csv, delimiter=";")

            while start_index > 0:
                next(link_reader)
                start_index -= 1

            for row in link_reader:
                # Clean the mun name
                mun_name = clean_mun_name(row[1])
                ibge_logger.debug("Cleaned the mun name and got %s.", mun_name)

                ibge_logger.info("%.2f%% complete. %d/%d" % ((scraped_muns/muns_total)*100, scraped_muns, muns_total))
                ibge_logger.info("Scraping %s ~ %s..." % (row[0], mun_name))

                # Get the brief html
                brief_html = insistent_request(row[3])

                # Get the info html
                info_html = insistent_request(row[4])

                # Scrape the brief
                brief_scr = MunScraper(brief_html)
                brief = brief_scr.as_dict()

                # Scrape the info
                info_scr = MunInfoScraper(info_html)
                info = info_scr.as_dict()

                ibge_logger.debug("Got %s for brief info." % str(brief))
                ibge_logger.debug("Got %s for detailed info." % str(info))

                # Write the data to the csv file
                write_data = [row[0], mun_name, brief["cod_mun"], brief["pop_estimada"], info["pib"]]
                mun_writer.writerow(write_data)

                # Count the scraped mun
                scraped_muns += 1

            ibge_logger.info("Scraped %d municipios to municipios.csv." % muns_total)


if __name__ == "__main__":
    scrape_muns()
