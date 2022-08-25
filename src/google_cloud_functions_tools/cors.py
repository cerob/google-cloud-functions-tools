from functools import partial, wraps


def cors(request_handler=None,
         *,
         origin='*',
         methods='POST',
         headers=None,
         max_age=3600):
    # https://github.com/dabeaz/python-cookbook/blob/master/src/9/defining_a_decorator_that_takes_an_optional_argument/example.py

    if request_handler is None:
        return partial(cors,
                       origin=origin,
                       methods=methods,
                       headers=headers,
                       max_age=max_age)

    if origin == '*':
        import warnings
        warnings.warn(
            'Setting Access-Control-Allow-Origin header to \'*\' is discouraged. '
            'It should not be used in production environments.')

    @wraps(request_handler)
    def wrapper(request, *args, **kwargs):
        _headers = {}
        if origin is not None:
            _headers['Access-Control-Allow-Origin'] = origin
        if methods is not None:
            _headers['Access-Control-Allow-Methods'] = methods
        if headers is not None:
            _headers['Access-Control-Allow-Headers'] = headers
        if max_age is not None:
            _headers['Access-Control-Max-Age'] = max_age

        if request.method == 'OPTIONS':
            return ('', 204, _headers)

        rv = request_handler(request, *args, **kwargs)

        # We reference make_response of Flask:
        # https://github.com/pallets/flask/blob/36af821edf741562cdcb6c60d63f23fa9a1d8776/src/flask/app.py#L2052
        if isinstance(rv, tuple):
            len_rv = len(rv)
            if len_rv == 3:
                # it is (body, status, headers) triplet
                body, status, existing_headers = rv
                existing_headers.update(_headers)
                return body, status, existing_headers
            elif len_rv == 2:
                if isinstance(rv[1], int):
                    # it is (body, status) pair
                    return *rv, _headers
                else:
                    # it is (body, headers) pair
                    body, existing_headers = rv
                    existing_headers.update(_headers)
                    return body, existing_headers
            elif len_rv == 1:
                return rv[0], _headers
            else:
                raise TypeError(
                    'The decorated function did not return a valid response.'
                    'See https://flask.palletsprojects.com/en/latest/quickstart/#about-responses'
                )
        else:
            return rv, _headers

    return wrapper
