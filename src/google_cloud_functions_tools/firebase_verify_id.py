from functools import partial, wraps

import firebase_admin
from firebase_admin import auth


def verify_firebase_id_token(request_handler=None,
                             *,
                             app_name='[DEFAULT]',
                             log=False):
    if request_handler is None:
        return partial(verify_firebase_id_token, app_name=app_name, log=log)

    @wraps(request_handler)
    def wrapper(request, *args, **kwargs):
        # https://github.com/firebase/functions-samples/blob/main/authorized-https-endpoint/functions/index.js

        if 'Authorization' not in request.headers:
            return 'Authorization header is required', 400  # Bad Request

        token = request.headers['Authorization'].strip('Bearer').strip()
        if token is None or token == '':
            return 'Bearer token is missing', 401  # Unauthorized

        try:
            firebase_admin.get_app(name=app_name)
        except ValueError as e:
            firebase_admin.initialize_app(name=app_name)

        try:
            # https://firebase.google.com/docs/auth/admin/verify-id-tokens#python
            # https://github.com/firebase/firebase-admin-python/blob/master/firebase_admin/_token_gen.py
            token_info = auth.verify_id_token(token)
        except firebase_admin._token_gen.ExpiredIdTokenError:
            return 'Token has expired', 401  # Unauthorized
        except firebase_admin._auth_utils.InvalidIdTokenError:
            return 'Token is invalid', 401  # Unauthorized

        if 'uid' not in token_info:
            return 'Undefined user', 401  # Unauthorized

        if log:
            # For cloud functions, we simply use print.
            # A cloud functions compatible logger can be developed here.
            name = token_info.get('name', '')
            email = token_info.get('email', '')
            print(f'Authenticated for name="{name}", email="{email}"')

        return request_handler(request, token_info, *args, **kwargs)

    return wrapper
