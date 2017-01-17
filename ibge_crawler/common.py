from urllib.request import urlopen


def utf8_request(url: str) -> str:
    response = urlopen(url)
    response_buf = response.read()
    return response_buf.decode()
