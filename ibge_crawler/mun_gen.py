import re

from ibge_crawler.common import utf8_request
from ibge_crawler.states import IBGEStates


class MunGenerator:
    # Config variables
    STATE_URL = "http://cidades.ibge.gov.br/xtras/uf.php?lang=&coduf=%d"
    MUN_EXTRACT_REGEX = r'perfil\.php\?lang=&codmun=(\d{6})&search=.+?\|(.+?)"'

    # Generate a state query url
    def _sturl_by_ibst(self, state: IBGEStates) -> str:
        return self.STATE_URL % state.value[0]

    def extract_mun_code(self, state: IBGEStates):
        url = self._sturl_by_ibst(state)
        html = utf8_request(url)

        # Make a list of tuples with (cod_mun, name)
        muns = re.findall(self.MUN_EXTRACT_REGEX, html)

        return muns
