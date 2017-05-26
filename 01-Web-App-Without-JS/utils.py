from auth0.v3.exceptions import Auth0Error


def safe_auth0_call(auth0_func, **auth0_kwargs):
    """
    Make a standard auth0 call based on arguments, but with improved error handling.
    Can handle inconsistent auth0 API error responses that are not caught by the `auth0-python` lib.
    """
    try:
        res = auth0_func(**auth0_kwargs)
    except KeyError as err:
        # Detect inconsistent Auth0 errors that do not have an 'error_description' key
        if err.args[0] == 'error_description':
            raise Auth0Error(status_code='', error_code='', message='')
        raise err

    # Detect inconsistent Auth0 errors that do not have an 'error' key
    if 'statusCode' in res and res['statusCode'] >= 400:
        raise Auth0Error(status_code='', error_code='', message='')

    return res
