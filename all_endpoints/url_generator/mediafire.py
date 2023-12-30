from typing import Union
from lxml import html
from requests import get as requests_get


def run(_id: str) -> Union[str, None]:
    try:
        resp = requests_get(f'https://www.mediafire.com/file/{_id}', allow_redirects=True, timeout=10)
        tree = html.fromstring(resp.content)
        data = tree.xpath('//a[@id="downloadButton"]/@href')[0]
        data = str(data[:data.rfind('/')])
    except Exception:
        data = None

    return data
