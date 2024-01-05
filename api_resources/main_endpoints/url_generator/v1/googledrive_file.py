from typing import Union
from httpx import get as httpx_get
from lxml import html


def main(_id: str) -> Union[str, None]:
    url = f'https://drive.google.com/uc?export=download&id={_id}'
    resp = httpx_get(url, follow_redirects=False, timeout=5)

    try:
        tree = html.fromstring(resp.content)
        data = tree.xpath('//form[@id="download-form"]/@action')[0]
    except Exception:
        data = url

    return data
