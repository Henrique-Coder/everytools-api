from typing import Union
from requests import get as requests_get
from lxml import html


def main(_id: str) -> Union[str, None]:
    try:
        resp = requests_get(f'https://drive.google.com/uc?id={_id}', allow_redirects=False, timeout=5)
        tree = html.fromstring(resp.content)
        data = tree.xpath('//form[@id="download-form"]/@action')[0]
    except Exception:
        data = None

    return data
