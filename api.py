from flask import Flask, request, jsonify
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_caching import Cache
from typing import Any
from re import compile, match

from api_resources.tools_endpoints.url_generator.v1.mediafire import main as url_generator__mediafire
from api_resources.tools_endpoints.url_generator.v1.googledrive import main as url_generator__googledrive

from api_resources.tools_endpoints.wrapper.v1.aliexpress import main as wrapper__aliexpress

from api_resources.tools_endpoints.randomizer.v1.random_int_number import main as randomizer__random_int_number
from api_resources.tools_endpoints.randomizer.v1.random_float_number import main as randomizer__random_float_number


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
def home() -> jsonify:
    return jsonify({
        'message': 'Welcome to the EveryTools API. Where you can find all the tools you need in one place.',
        'author_github': 'https://github.com/Henrique-Coder',
        'source_code_url': 'https://github.com/Henrique-Coder/everytools-api',
        'base_url': 'http://node1.mindwired.com.br:8452',
        'endpoints': {
            'url-generator': {
                'mediafire': {
                    'url': '/url-generator/v1/mediafire?id=',
                    'description': 'Generates a direct download link for items hosted on MediaFire.',
                    'rate_limit': '1/second;30/minute;200/hour;600/day',
                },
                'googledrive': {
                    'url': '/url-generator/v1/googledrive?id=',
                    'description': 'Generates a direct download link for items hosted on Google Drive.',
                    'rate_limit': '1/second;30/minute;200/hour;600/day',
                }
            },
            'wrapper': {
                'aliexpress-product': {
                    'url': '/wrapper/v1/aliexpress-product?id=',
                    'description': 'Wraps AliExpress product info into a friendly JSON format.',
                    'rate_limit': '1/second;30/minute;200/hour;600/day',
                }
            },
            'randomizer': {
                'random-int-number': {
                    'url': '/randomizer/v1/random-int-number?min=&max=',
                    'description': 'Generates a random integer number between two numbers.',
                    'rate_limit': '5/second;5000/day',
                },
                'random-float-number': {
                    'url': '/randomizer/v1/random-float-number?min=&max=',
                    'description': 'Generates a random float number between two numbers.',
                    'rate_limit': '5/second;5000/day',
                }
            }
        }
    }), 200


# Flask API routes

# Route: /url-generator/mediafire -> Generates a direct download link for items hosted on MediaFire.
@app.route('/url-generator/v1/mediafire', methods=['GET'])
@limiter.limit('1/second;30/minute;200/hour;600/day')
@cache.cached(timeout=300, make_cache_key=_make_cache_key)
def _url_generator__mediafire() -> jsonify:
    p_id = request.args.get('id')

    if not p_id or not p_id.isalnum():
        return jsonify({'success': False, 'message': "The id parameter is required and must be alphanumeric."}), 400

    output_data = url_generator__mediafire(p_id)

    if output_data:
        return jsonify({'success': True, 'url': output_data, 'query': {'id': p_id}}), 200
    else:
        return jsonify({'success': False, 'message': 'Query not found or invalid. Please check your query and try again.', 'query': {'id': p_id}}), 404


# Route: /url-generator/googledrive -> Generates a direct download link for items hosted on Google Drive.
@app.route('/url-generator/v1/googledrive', methods=['GET'])
@limiter.limit('1/second;30/minute;200/hour;600/day')
@cache.cached(timeout=300, make_cache_key=_make_cache_key)
def _url_generator__googledrive() -> jsonify:
    p_id = request.args.get('id')

    if not p_id or not compile(r'^[a-zA-Z0-9_-]+$').match(p_id):
        return jsonify({'success': False, 'message': "The id parameter is required and must be alphanumeric."}), 400

    output_data = url_generator__googledrive(p_id)

    if output_data:
        return jsonify({'success': True, 'url': output_data, 'query': {'id': p_id}}), 200
    else:
        return jsonify({'success': False, 'message': 'Query not found or invalid. Please check your query and try again.', 'query': {'id': p_id}}), 404


# Route: /wrapper/aliexpress-product -> Wraps AliExpress product info into a friendly JSON format.
@app.route('/wrapper/v1/aliexpress-product', methods=['GET'])
@limiter.limit('1/second;30/minute;200/hour;600/day')
@cache.cached(timeout=300, make_cache_key=_make_cache_key)
def _wrapper__aliexpress_product() -> jsonify:
    p_id = request.args.get('id')

    if not p_id or not p_id.isnumeric():
        return jsonify({'success': False, 'message': "The id parameter is required and must be numeric."}), 400

    p_id = int(p_id)
    output_data = wrapper__aliexpress(p_id)

    if output_data:
        return jsonify({'success': True, 'product': output_data, 'query': {'id': p_id}}), 200
    else:
        return jsonify({'success': False, 'message': 'Query not found or invalid. Please check your query and try again.', 'query': {'id': p_id}}), 404


# Route: /randomizer/random-int-number -> Generates a random integer number between two numbers.
@app.route('/randomizer/v1/random-int-number', methods=['GET'])
@limiter.limit('5/second;5000/day')
def _randomizer__random_int_number() -> jsonify:
    p_min = request.args.get('min')
    p_max = request.args.get('max')

    if not p_min or not p_min.isnumeric() or not p_max or not p_max.isnumeric():
        return jsonify({'success': False, 'message': "The min and max parameters are required and must be integers."}), 400

    p_min, p_max = int(p_min), int(p_max)
    if p_min > p_max:
        return jsonify({'success': False, 'message': "The min parameter must be less than the max parameter."}), 400

    output_data = randomizer__random_int_number(p_min, p_max)

    if output_data:
        return jsonify({'success': True, 'number': output_data, 'type': 'int', 'query': {'min': p_min, 'max': p_max}}), 200
    else:
        return jsonify({'success': False, 'message': 'An error occurred while generating the random number. Please check your query and try again.', 'query': {'min': p_min, 'max': p_max}}), 404


# Route: /randomizer/random-float-number -> Generates a random float number between two numbers.
@app.route('/randomizer/v1/random-float-number', methods=['GET'])
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

    if not p_min or not is_float(p_min) or not p_max or not is_float(p_max):
        return jsonify({'success': False, 'message': "The min and max parameters are required and must be floats."}), 400

    p_min, p_max = float(p_min), float(p_max)
    if p_min > p_max:
        return jsonify({'success': False, 'message': "The min parameter must be less than the max parameter."}), 400

    output_data = randomizer__random_float_number(float(p_min), float(p_max))

    if output_data:
        return jsonify({'success': True, 'number': output_data, 'type': 'float', 'query': {'min': p_min, 'max': p_max}}), 200
    else:
        return jsonify({'success': False, 'message': 'An error occurred while generating the random number. Please check your query and try again.', 'query': {'min': p_min, 'max': p_max}}), 404


if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', threaded=True, port=8452)
