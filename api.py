from flask import Flask, request, jsonify
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_caching import Cache
from typing import Any, Union

from api_endpoints.v1.url_generator.mediafire import main as url_generator__mediafire
from api_endpoints.v1.url_generator.googledrive import main as url_generator__googledrive

from api_endpoints.v1.randomizer.random_int_number import main as randomizer__random_int_number
from api_endpoints.v1.randomizer.random_float_number import main as randomizer__random_float_number

from api_endpoints.v1.wrapper.aliexpress import main as wrapper__aliexpress


# Initialize Flask app and your plugins
app = Flask(__name__)
app.config['JSON_SORT_KEYS'] = True
app.config['CACHE_TYPE'] = 'simple'
limiter = Limiter(app=app, key_func=get_remote_address, storage_uri='memory://')
cache = Cache(app)


# Flask required functions
def _make_cache_key(*args, **kwargs) -> str:
    return f'{request.url}{str(request.args)}'


# Flask error handlers
@app.errorhandler(404)
@cache.cached(timeout=86400, make_cache_key=_make_cache_key)
def weberror_404(_) -> jsonify:
    return jsonify({'success': False, 'message': 'Endpoint not found. Please check your endpoint and try again.'}), 404


# Flask general routes
@app.route('/')
@cache.cached(timeout=86400, make_cache_key=_make_cache_key)
def index() -> jsonify:
    return jsonify({
        'success': True,
        'message': 'Welcome to the EveryTools API. Please check the documentation for more information.',
        'documentation_url': '',
        'version': '1',
        'author_github': 'https://github.com/Henrique-Coder',
        'source_code_url': 'https://github.com/Henrique-Coder/everytools-api',
        'endpoints': {
            'url-generator': {
                'mediafire': {
                    'url': '/url-generator/mediafire?id=',
                    'description': 'Generates a direct download link for items hosted on MediaFire.',
                    'rate_limit': '1/second;30/minute;200/hour;600/day',
                },
                'googledrive': {
                    'url': '/url-generator/googledrive?id=',
                    'description': 'Generates a direct download link for items hosted on Google Drive.',
                    'rate_limit': '1/second;30/minute;200/hour;600/day',
                }
            },
            'wrapper': {
                'aliexpress-product': {
                    'url': '/wrapper/aliexpress-product?id=',
                    'description': 'Wraps AliExpress product info into a friendly JSON format.',
                    'rate_limit': '1/second;30/minute;200/hour;600/day',
                }
            },
            'randomizer': {
                'random-int-number': {
                    'url': '/randomizer/random-int-number?min=&max=',
                    'description': 'Generates a random integer number between two numbers.',
                    'rate_limit': '5/second;5000/day',
                },
                'random-float-number': {
                    'url': '/randomizer/random-float-number?min=&max=',
                    'description': 'Generates a random float number between two numbers.',
                    'rate_limit': '5/second;5000/day',
                }
            }
        }
    })


# Flask API routes

# Route: /url-generator/mediafire -> Generates a direct download link for items hosted on MediaFire.
@app.route('/url-generator/mediafire', methods=['GET'])
@limiter.limit('1/second;30/minute;200/hour;600/day')
@cache.cached(timeout=300, make_cache_key=_make_cache_key)
def _url_generator__mediafire() -> jsonify:
    p_id = request.args.get('id')

    if not p_id or not p_id.isalnum():
        return jsonify({'success': False, 'message': "The id parameter is required, must exist and must be alphanumeric."}), 400

    output_data = url_generator__mediafire(p_id)

    if output_data:
        return jsonify({'success': True, 'url': output_data, 'query': {'id': p_id}}), 200
    else:
        return jsonify({'success': False, 'message': 'Query not found or invalid. Please check your query and try again.', 'query': {'id': p_id}}), 404


# Route: /url-generator/googledrive -> Generates a direct download link for items hosted on Google Drive.
@app.route('/url-generator/googledrive', methods=['GET'])
@limiter.limit('1/second;30/minute;200/hour;600/day')
@cache.cached(timeout=300, make_cache_key=_make_cache_key)
def _url_generator__googledrive() -> jsonify:
    p_id = request.args.get('id')

    if not p_id or not p_id.isalnum():
        return jsonify({'success': False, 'message': "The id parameter is required, must exist and must be alphanumeric."}), 400

    output_data = url_generator__googledrive(p_id)

    if output_data:
        return jsonify({'success': True, 'url': output_data, 'query': {'id': p_id}}), 200
    else:
        return jsonify({'success': False, 'message': 'Query not found or invalid. Please check your query and try again.', 'query': {'id': p_id}}), 404


# Route: /wrapper/aliexpress-product -> Wraps AliExpress product info into a friendly JSON format.
@app.route('/wrapper/aliexpress-product', methods=['GET'])
@limiter.limit('1/second;30/minute;200/hour;600/day')
@cache.cached(timeout=300, make_cache_key=_make_cache_key)
def _wrapper__aliexpress_product() -> jsonify:
    p_id = request.args.get('id')

    if not p_id or not p_id.isnumeric():
        return jsonify({'success': False, 'message': "The id parameter is required, must exist and must be numeric."}), 400

    output_data = wrapper__aliexpress(p_id)

    if output_data:
        return jsonify({'success': True, 'product': output_data, 'query': {'id': p_id}}), 200
    else:
        return jsonify({'success': False, 'message': 'Query not found or invalid. Please check your query and try again.', 'query': {'id': p_id}}), 404


# Route: /randomizer/random-int-number -> Generates a random integer number between two numbers.
@app.route('/randomizer/random-int-number', methods=['GET'])
@limiter.limit('5/second;5000/day')
def _randomizer__random_int_number() -> jsonify:
    p_min = request.args.get('min')
    p_max = request.args.get('max')

    if not p_min or not p_min.isnumeric() or not p_max or not p_max.isnumeric() or p_min > p_max:
        return jsonify({'success': False, 'message': "The min and max parameters are required, must exist and must be numeric. The min parameter must be less than the max parameter."}), 400

    output_data = randomizer__random_int_number(int(p_min), int(p_max))

    if output_data:
        return jsonify({'success': True, 'number': output_data, 'type': 'int', 'query': {'min': p_min, 'max': p_max}}), 200
    else:
        return jsonify({'success': False, 'message': 'An error occurred while generating the random number. Please check your query and try again.', 'query': {'min': p_min, 'max': p_max}}), 404


# Route: /randomizer/random-float-number -> Generates a random float number between two numbers.
@app.route('/randomizer/random-float-number', methods=['GET'])
@limiter.limit('5/second;5000/day')
def _randomizer__random_float_number() -> jsonify:
    def is_float(value: Any) -> bool:
        try:
            float(value)
            return True
        except Exception:
            return False

    p_min = request.args.get('min')
    p_max = request.args.get('max')

    if not p_min or not is_float(p_min) or not p_max or not is_float(p_max) or float(p_min) > float(p_max):
        return jsonify({'success': False, 'message': "The min and max parameters are required, must exist and must be integer or float numbers. The min parameter must be less than the max parameter."}), 400

    output_data = randomizer__random_float_number(float(p_min), float(p_max))

    if output_data:
        return jsonify({'success': True, 'number': output_data, 'type': 'float', 'query': {'min': p_min, 'max': p_max}}), 200
    else:
        return jsonify({'success': False, 'message': 'An error occurred while generating the random number. Please check your query and try again.', 'query': {'min': p_min, 'max': p_max}}), 404


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', threaded=True, port=8452)
