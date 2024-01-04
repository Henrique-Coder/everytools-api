from typing import Union
from requests import get as requests_get
from lxml import html


def main(_id: str) -> Union[str, None]:
    try:
        url = f'https://drive.google.com/uc?export=download&id={_id}'
        resp = requests_get(url, allow_redirects=False, timeout=5)

        try:
            tree = html.fromstring(resp.content)
            data = tree.xpath('//form[@id="download-form"]/@action')[0]
        except Exception:
            return url

    except Exception:
        data = None

    return data
