# Google Cloud Functions Tools
A set of utility functions are provided, especially developed for Google Cloud Functions (might work on other serverless platforms too). The functions planned are mostly to be decorators.

## CORS
Adds CORS headers to your function. Responds to `OPTIONS` request by sending CORS headers and without triggering the cloud function. Provided that Google Cloud Funtions use Flask for underlying logic, the return types must be compatible with Flask's.

For example:
```python
from google_cloud_functions_tools import cors

@cors
def run(request):
    return 'Response text'
```

sets the following headers by default:
```
Access-Control-Allow-Origin: '*'
Access-Control-Allow-Methods: 'POST'
Access-Control-Allow-Headers: ''
Access-Control-Max-Age: 3600
```

However, these default values might change at any time, therefore it is better to specify headers explicitly:
```python
from google_cloud_functions_tools import cors

@cors(origin='sample_origin',
      methods='GET',
      headers='Content-Type',
      max_age=9600)
def run(request):
    return 'Response text', 200
```

sets the following headers:
```
Access-Control-Allow-Origin: 'sample_origin'
Access-Control-Allow-Methods: 'GET'
Access-Control-Allow-Headers: 'Content-Type'
Access-Control-Max-Age: 9600
```

The method warns if `Access-Control-Allow-Origin` header is set to `'*'`:
```
UserWarning: Setting Access-Control-Allow-Origin header to '*' is discouraged. It should not be used in production environments.
```

## Verify Firebase ID Token
Authenticates Firebase sessions in cloud functions using `firebase_admin`'s `auth.verify_id_token` function. A request is required to provide `Authorization: Bearer <token>` HTTP header.

If authentication fails, an HTTP 401 Unauthorized error is returned without running the actual function. If an Authorization header is not supplied, an HTTP 400 Bad Request is returned immediately. In case of successful authorization, token information is sent to the actual function as a second argument (after request object).

```python
from google_cloud_functions_tools import verify_firebase_id_token

@verify_firebase_id_token
def run(request, token_info):
    return token_info
```

`app_name` argument passes app name to `firebase_admin` library. The default value is `[DEFAULT]`.

```python
from google_cloud_functions_tools import verify_firebase_id_token

@verify_firebase_id_token(app_name='[DEFAULT]')
def run(request, token_info):
    return token_info
```

Setting `log` argument to `True` logs user information to cloud function logs.

```python
from google_cloud_functions_tools import verify_firebase_id_token

@verify_firebase_id_token(log=True)
def run(request, token_info):
    return token_info
```

logs:

```
Authenticated for name="Someone", email="someone@example.com"
```

## Contibuting
Pull requests and issues are welcomed. New functions are planned to be added in time when they are needed.
