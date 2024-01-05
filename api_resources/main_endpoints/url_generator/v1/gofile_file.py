from typing import Union, Any
from httpx import get as httpx_get
from lxml import html


def main(_id: str) -> Union[Any, None]:
    url = f'https://gofile.io/d/{_id}'
    resp = httpx_get(url, follow_redirects=False, timeout=5)

    try:
        tree = html.fromstring(resp.content)
        data = None

    except Exception:
        return None

    return data
