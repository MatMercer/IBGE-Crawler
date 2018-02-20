# IBGE-Crawler
Um crawler simples do IBGE implementado em Python 3. Criado 
em Janeiro de 2017. Como todos os Crawlers estendem a Classe
DictoClosured, é muito fácil de adicionar novos campos para minerar, por 
exemplo, atualmente somente esses dados são minerados:

**MunScraper**
```python
    def pop_estimada(self):
        data = self._data_by_alike_text("População estimada").replace(".", "")

        return int(data)

    def cod_mun(self):
        data = self._data_by_alike_text("Código do Mun")

        return int(data)
```

**MunInfoScraper**
```python
    def pib(self):
        data = self._data_by_alike_text("PIB per capita")

        return self._float_data(data)
```

## Como usar?

[![asciicast](https://asciinema.org/a/qDMWWyZNx1jqZq061vjwzgA28.png)](https://asciinema.org/a/qDMWWyZNx1jqZq061vjwzgA28)

## Por que o código esta em portugues e em inglês?!
Não sei ¯\\_(ツ)_/¯ acontece.
