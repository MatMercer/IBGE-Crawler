import re

from ibge_crawler.common import utf8_request, ibge_logger
from ibge_crawler.states import IBGEStates


class MunGenerator:
    # Config variables
    STATE_URL = "http://cidades.ibge.gov.br/xtras/uf.php?lang=&coduf=%d"
    MUN_MAIN_URL = "http://cidades.ibge.gov.br/xtras/perfil.php?lang=&codmun=%s"
    MUN_INFO_URL = "http://cidades.ibge.gov.br/xtras/temas.php?lang=&codmun=%s&idtema=16"
    MUN_EXTRACT_REGEX = re.compile(r'perfil\.php\?lang=&codmun=(\d{6})&search=.+?\|(.+?)"')

    # Generate a state query url
    def _sturl_by_ibst(self, state: IBGEStates) -> str:
        return self.STATE_URL % state.value[0]

    def extract_mun_codes(self, state: IBGEStates):
        url = self._sturl_by_ibst(state)
        ibge_logger.debug("Opening %s..." % url)
        html = utf8_request(url)

        # Make a list of tuples with (cod_mun, name)
        muns = self.MUN_EXTRACT_REGEX.findall(html)

        return muns

    def gen_mun_urls(self, mun_code: str):
        return self.MUN_MAIN_URL % mun_code, self.MUN_INFO_URL % mun_code
