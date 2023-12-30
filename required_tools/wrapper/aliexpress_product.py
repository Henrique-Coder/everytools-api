from json import loads as json_loads
from re import compile as re_compile
from typing import Union
from urllib.parse import urljoin as urllib_parse_urljoin
from bs4 import BeautifulSoup
from requests import get as requests_get


def run(_id: str) -> Union[dict, None]:
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, como Gecko) Chrome/115.0.0.0 Safari/537.36',
        'Accept-Language': 'en-US',
    }

    try:
        page_content = requests_get(f'https://www.aliexpress.com/item/{_id}.html', headers=headers).content
        soup = BeautifulSoup(page_content, 'html.parser')
        data = soup.find('script', string=re_compile(r'window.runParams\s*=\s*{')).string.strip().replace('\n', str())
        raw_data = dict(json_loads(data[data.find('{', data.find('{') + 1): data.rfind('}')], strict=True))
    except Exception:
        return None

    _c1 = json_loads(raw_data['priceComponent']['skuJson'])[0]
    _c2 = raw_data['storeHeaderComponent']['storeHeaderResult']['tabList']
    _c3 = raw_data['sellerComponent']
    _c4 = raw_data['productInfoComponent']

    formatted_dict = {
        'storeInfo': {
            'id': int(_c3['storeNum']),
            'name': str(raw_data['storeHeaderComponent']['storeHeaderResult']['storeName']),
            'homepageUrl': str('https:' + urllib_parse_urljoin(str(), _c2[0]['url'])),
            'productsUrl': str('https:' + urllib_parse_urljoin(str(), _c2[1]['url'])),
            'promotionsUrl': str('https:' + urllib_parse_urljoin(str(), _c2[2]['url'])),
            'bestSellersUrl': str('https:' + urllib_parse_urljoin(str(), _c2[3]['url'])),
            'reviewsUrl': str('https:' + urllib_parse_urljoin(str(), _c2[4]['url'])),
            'logoUrl': str(urllib_parse_urljoin(str(), _c3['storeLogo'])),
        },
        'productInfo': {
            'id': int(_c4['id']),
            'name': str(_c4['subject']),
            'descriptionUrl': str(raw_data['productDescComponent']['descriptionUrl']),
            'availableStock': int(_c1['skuVal']['availQuantity']),
        },
        'productPrice': {
            'currencyCode': str(_c1['skuVal']['skuAmount']['currency']),
            'originalValue': round(float(_c1['skuVal']['skuAmount']['value']), 2),
            'discountPercentage': round(float(_c1['skuVal']['discount']), 2),
            'finalPrice': round(float(_c1['skuVal']['skuActivityAmount']['value']), 2),
        }
    }

    return formatted_dict
