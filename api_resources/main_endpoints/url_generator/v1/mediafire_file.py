from typing import Union
from requests import get as requests_get
from lxml import html


def main(_id: str) -> Union[str, None]:
    try:
        resp = requests_get(f'https://www.mediafire.com/file/{_id}', allow_redirects=False, timeout=5)
        tree = html.fromstring(resp.content)
        data = tree.xpath('//a[@id="downloadButton"]/@href')[0]
        data = str(data[:data.rfind('/')])
    except Exception:
        data = None

    return data
