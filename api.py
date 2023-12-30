from flask import Flask, request, jsonify
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from re import sub as re_sub
from typing import Any

from all_endpoints.url_generator.mediafire import run as generator_mediafire
from all_endpoints.url_generator.googledrive import run as generator_googledrive

from all_endpoints.wrapper.aliexpress_product import run as wrapper_aliexpress_product

from all_endpoints.randomizer.random_int_number import run as randomizer_random_int_number
from all_endpoints.randomizer.random_float_number import run as randomizer_random_float_number


# Initialize Flask and Flask-Limiter
app = Flask(__name__)
app.config['JSON_SORT_KEYS'] = True
limiter = Limiter(app=app, key_func=get_remote_address, storage_uri='memory://')


def show_empty_required_param_error(message: str) -> jsonify:
    data = {'success': False, 'message': message}

    return jsonify(data), 400


def modify_string(string: Any, pattern: str) -> str:
    return re_sub(pattern, str(), str(string))


@app.errorhandler(404)
def weberror_404(_) -> jsonify:
    return jsonify({'success': False, 'message': 'Endpoint not found. Please check your endpoint and try again.'}), 404


@app.route('/')
def index() -> jsonify:
    return jsonify({
        'success': True,
        'message': 'Welcome to the EveryTools API. Please check the documentation for more information.',
        'documentation_url': '',
        'version': '1.0.0',
        'author_github': 'https://github.com/Henrique-Coder',
        'endpoints': {
            'url-generator': {
                'mediafire': {
                    'url': '/url-generator/mediafire?id=',
                    'description': 'MediaFire direct download url generator.',
                    'rate_limit': '1/second;30/minute;200/hour;600/day',
                },
                'googledrive': {
                    'url': '/url-generator/googledrive?id=',
                    'description': 'Google Drive direct download url generator.',
                    'rate_limit': '1/second;30/minute;200/hour;600/day',
                }
            },
            'wrapper': {
                'aliexpress-product': {
                    'url': '/wrapper/aliexpress-product?id=',
                    'description': 'AliExpress product info wrapper.',
                    'rate_limit': '1/second;30/minute;200/hour;600/day',
                }
            },
            'randomizer': {
                'random-int-number': {
                    'url': '/randomizer/random-int-number?min=&max=',
                    'description': 'Random integer number generator.',
                    'rate_limit': '5/second;5000/day',
                },
                'random-float-number': {
                    'url': '/randomizer/random-float-number?min=&max=',
                    'description': 'Random float number generator.',
                    'rate_limit': '5/second;5000/day',
                }
            }
        }
    })


########################################################################################################################

# API: Generator - MediaFire direct download url
@app.route('/url-generator/mediafire', methods=['GET'])
@limiter.limit('1/second;30/minute;200/hour;600/day')
def url_generator__mediafire() -> Any:
    param_id = request.args.get('id')

    if not param_id:
        return show_empty_required_param_error("Parameter 'id' is required and cannot be empty, non-existent or non-alphanumeric.")

    param_id = modify_string(request.args.get('id'), r'[^a-zA-Z0-9]')

    if not param_id:
        return show_empty_required_param_error("Parameter 'id' is required and cannot be empty, non-existent or non-alphanumeric.")

    output_data = generator_mediafire(param_id)

    if output_data:
        data = {'success': True, 'url': output_data, 'query': param_id}
        return jsonify(data)
    else:
        data = {'success': False, 'message': 'Query not found or invalid. Please check your query and try again.', 'query': param_id}
        return jsonify(data), 404


# API: Generator - Google Drive direct download url
@app.route('/url-generator/googledrive', methods=['GET'])
@limiter.limit('1/second;30/minute;200/hour;600/day')
def url_generator__googledrive() -> Any:
    param_id = request.args.get('id')

    if not param_id:
        return show_empty_required_param_error("Parameter 'id' is required and cannot be empty, non-existent or non-alphanumeric.")

    param_id = modify_string(request.args.get('id'), r'[^a-zA-Z0-9\-_]')

    if not param_id:
        return show_empty_required_param_error("Parameter 'id' is required and cannot be empty, non-existent or non-alphanumeric.")

    output_data = generator_googledrive(param_id)

    if output_data:
        data = {'success': True, 'url': output_data, 'query': param_id}
        return jsonify(data)
    else:
        data = {'success': False, 'message': 'Query not found or invalid. Please check your query and try again.', 'query': param_id}
        return jsonify(data), 404


# API: Wrapper - AliExpress product info
@app.route('/wrapper/aliexpress-product', methods=['GET'])
@limiter.limit('1/second;30/minute;200/hour;600/day')
def wrapper__aliexpress_product() -> Any:
    param_id = request.args.get('id')

    if not param_id:
        return show_empty_required_param_error("Parameter 'id' is required and cannot be empty, non-existent or non-numerical.")

    param_id = modify_string(request.args.get('id'), r'\D')

    if not param_id:
        return show_empty_required_param_error("Parameter 'id' is required and cannot be empty, non-existent or non-numerical.")

    output_data = wrapper_aliexpress_product(param_id)

    if output_data:
        data = {'success': True, 'data': output_data, 'query': param_id}
        return jsonify(data)
    else:
        data = {'success': False, 'message': 'Query not found or invalid. Please check your query and try again.', 'query': param_id}
        return jsonify(data), 404


# API: Randomizer - Random int number
@app.route('/randomizer/random-int-number', methods=['GET'])
@limiter.limit('5/second;5000/day')
def randomizer__random_int_number() -> Any:
    param_min = request.args.get('min')
    param_max = request.args.get('max')

    if not param_min:
        return show_empty_required_param_error("Parameter 'min' is required and cannot be empty, non-existent or non-numerical.")

    if not param_max:
        return show_empty_required_param_error("Parameter 'max' is required and cannot be empty, non-existent or non-numerical.")

    param_min = modify_string(request.args.get('min'), r'[^\d.]')
    param_max = modify_string(request.args.get('max'), r'[^\d.]')

    if not param_min or '.' in param_min:
        return show_empty_required_param_error("Parameter 'min' is required and cannot be empty, non-existent or non-numerical.")

    if not param_max or '.' in param_max:
        return show_empty_required_param_error("Parameter 'max' is required and cannot be empty, non-existent or non-numerical.")

    output_data = randomizer_random_int_number(int(param_min), int(param_max))

    if output_data:
        data = {'success': True, 'number': output_data, 'type': type(output_data).__name__, 'query': {'min': param_min, 'max': param_max}}
        return jsonify(data)
    else:
        data = {'success': False, 'message': 'Min and max value should be an integer number. Please check your query and try again.', 'query': {'min': param_min, 'max': param_max}}
        return jsonify(data), 404


# API: Randomizer - Random float number
@app.route('/randomizer/random-float-number', methods=['GET'])
@limiter.limit('5/second;5000/day')
def randomizer__random_float_number() -> Any:
    param_min = request.args.get('min')
    param_max = request.args.get('max')

    if not param_min:
        return show_empty_required_param_error("Parameter 'min' is required and cannot be empty, non-existent or non-numerical (dot is allowed).")

    if not param_max:
        return show_empty_required_param_error("Parameter 'max' is required and cannot be empty, non-existent or non-numerical (dot is allowed).")

    param_min = modify_string(request.args.get('min'), r'[^\d.]')
    param_max = modify_string(request.args.get('max'), r'[^\d.]')

    if not param_min or '.' not in param_min or param_min.count('.') > 1 or param_min.startswith('.') or param_min.endswith('.'):
        return show_empty_required_param_error("Parameter 'min' is required and cannot be empty, non-existent or non-numerical (dot is allowed).")

    if not param_max or '.' not in param_max or param_max.count('.') > 1 or param_max.startswith('.') or param_max.endswith('.'):
        return show_empty_required_param_error("Parameter 'max' is required and cannot be empty, non-existent or non-numerical (dot is allowed).")

    output_data = randomizer_random_float_number(float(param_min), float(param_max))

    if output_data:
        data = {'success': True, 'number': output_data, 'type': type(output_data).__name__, 'query': {'min': param_min, 'max': param_max}}
        return jsonify(data)
    else:
        data = {'success': False, 'message': 'Min and max value should be a float number. Please check your query and try again.', 'query': {'min': param_min, 'max': param_max}}
        return jsonify(data), 404


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', threaded=True, port=8452)
