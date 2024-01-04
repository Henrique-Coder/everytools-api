from typing import Union, Any
from requests import get as requests_get
from lxml import html


def main(_id: str) -> Union[Any, None]:
    url = f'https://gofile.io/d/{_id}'
    resp = requests_get(url, allow_redirects=False, timeout=5)

    try:
        tree = html.fromstring(resp.content)
        data = None

    except Exception:
        return None

    return data
