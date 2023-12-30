from typing import Union
from lxml import html
from requests import get as requests_get


def run(_id: str) -> Union[str, None]:
    try:
        resp = requests_get(f'https://drive.google.com/uc?id={_id}', allow_redirects=True, timeout=10)
        tree = html.fromstring(resp.content)
        data = tree.xpath('//form[@id="download-form"]/@action')[0]
    except Exception:
        data = None

    return data if data else None
