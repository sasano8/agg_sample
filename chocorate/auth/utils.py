from typing import Literal
from requests.auth import HTTPBasicAuth, HTTPDigestAuth, HTTPProxyAuth
from requests_oauthlib import OAuth1, OAuth2Session


# requests.auth.AuthBase でカスタイマイズ可能

def make(_: Literal["basic", "digest", "oauth1", "oauth2"], **params):
    if _ == "basic":
        auth= HTTPBasicAuth('username', 'password')
    elif _ == "digest":
        auth = HTTPDigestAuth('username', 'password')
    elif _ == "oauth1":
        auth = OAuth1('client_key', 'client_secret', 'token', 'token_secret')
    elif _ == "oauth2":
        auth = OAuth2Session('client_id', token={'access_token': 'access_token', 'token_type': 'Bearer'})
    else:
        raise Exception()