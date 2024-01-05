from typing import Union
from httpx import get as httpx_get
from lxml import html


def main(_id: str) -> Union[str, None]:
    try:
        url = f'https://www.mediafire.com/file/{_id}'
        resp = httpx_get(url, follow_redirects=False, timeout=5)
        tree = html.fromstring(resp.content)
        data = tree.xpath('//a[@id="downloadButton"]/@href')[0]
        data = str(data[:data.rfind('/')])
    except Exception:
        data = None

    return data
