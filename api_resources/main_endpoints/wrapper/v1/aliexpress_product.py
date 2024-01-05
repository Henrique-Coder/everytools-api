from typing import Union
from re import compile as re_compile
from json import loads as json_loads
from httpx import get
from bs4 import BeautifulSoup
from urllib.parse import urljoin


def main(_id: int) -> Union[dict, None]:
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, como Gecko) Chrome/115.0.0.0 Safari/537.36',
        'Cookie': 'xman_f=82eZ73Yk3kUmArs2cqSaeVhIBpZUqa5s/nFuPNZUbJduW17e9ELWYOdwJD9yZAawfaLD8+Yi69pXnJy2qhqQWnyq5vD3lfKYXc8WGgVIsu4ExnaqS8zejw==;aep_usuc_f=site=usa&c_tp=USD&region=US&b_locale=en_US',
    }

    try:
        url = f'https://www.aliexpress.us/item/{_id}.html'
        resp = get(url, follow_redirects=True, headers=headers).content
        soup = BeautifulSoup(resp, 'html.parser')
        data = soup.find('script', string=re_compile(r'window.runParams\s*=\s*{')).string.strip().replace('\n', str())
        raw_data = dict(json_loads(data[data.find('{', data.find('{') + 1): data.rfind('}')], strict=True))
    except Exception:
        return None

    _c1 = json_loads(raw_data['priceComponent']['skuJson'])[0]
    _c2 = raw_data['storeHeaderComponent']['storeHeaderResult']['tabList']
    _c3 = raw_data['sellerComponent']

    formatted_data = {
        'store-info': {
            'id': int(_c3['storeNum']),
            'name': str(raw_data['storeHeaderComponent']['storeHeaderResult']['storeName']),
            'homepage-url': str('https:' + urljoin(str(), _c2[0]['url'])),
            'products-url': str('https:' + urljoin(str(), _c2[1]['url'])),
            'promotions-url': str('https:' + urljoin(str(), _c2[2]['url'])),
            'best-sellers-url': str('https:' + urljoin(str(), _c2[3]['url'])),
            'reviews-url': str('https:' + urljoin(str(), _c2[4]['url'])),
            'logo-url': str(urljoin(str(), _c3['storeLogo'])),
        },
        'product-info': {
            'id': int(_id),
            'url': f'https://www.aliexpress.com/item/{_id}.html',
            'name': str(raw_data['productInfoComponent']['subject']),
            'description-url': str(raw_data['productDescComponent']['descriptionUrl']),
            'available-stock': int(_c1['skuVal']['availQuantity']),
        },
        'product-price': {
            'currency-code': str(_c1['skuVal']['skuAmount']['currency']),
            'original-value': round(float(_c1['skuVal']['skuAmount']['value']), 2),
            'discount-percentage': round(float(_c1['skuVal']['discount']), 2),
            'final-price': round(float(_c1['skuVal']['skuActivityAmount']['value']), 2),
        }
    }

    return formatted_data
