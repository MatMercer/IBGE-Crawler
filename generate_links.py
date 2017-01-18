from csv import writer, reader

from ibge_crawler.common import ibge_logger
from ibge_crawler.mun_gen import MunGenerator
from ibge_crawler.states import IBGEStates


def generate_links():
    ibge_logger.debug("Opening links.csv...")

    # Total of municipios
    mun_total = 0

    # Open the file
    with open("links.csv", "w", newline="") as csvfile:
        # Create a csv writer
        link_writer = writer(csvfile)

        # Create a municipio link generator
        gen = MunGenerator()

        # Iterate over all states
        for state in IBGEStates:
            ibge_logger.info("Generating %s..." % state.value[1])

            # Get the municipio codes for this state
            muns = gen.extract_mun_codes(state)

            mun_total += len(muns)
            ibge_logger.info("Found %d municipios for %s." % (len(muns), state.name))

            ibge_logger.debug("Writing to links.csv.")
            # Write to the csv file
            for mun in muns:
                # Generate the links for this municipio
                links = gen.gen_mun_urls(mun[0])
                ibge_logger.debug("Generated %s links." % str(links))

                link_writer.writerow([state.name, mun[1], mun[0], links[0], links[1]])

        ibge_logger.info("Found a total of %d municipos.", mun_total)

if __name__ == "__main__":
    generate_links()
