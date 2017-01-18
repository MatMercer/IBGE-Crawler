from ibge_crawler.mun_gen import MunGenerator
from ibge_crawler.states import IBGEStates

state = IBGEStates.SP

mun_gen = MunGenerator()

muns = mun_gen.extract_mun_codes(state)

for mun in muns:
    print(mun)

print("%d municípios encontrados em %s." % (len(muns), state.value[1]))
