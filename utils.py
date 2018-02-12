import hashlib
import hmac
import urllib

import requests


def build_exx_sign(params, secret_key):
    sign = ''
    for key in sorted(params.keys()):
        sign += key + '=' + str(params[key]) + '&'
    if len(sign) > 0:
        sign = sign[0:-1]
    return hmac.new(secret_key.encode('utf-8'), sign.encode('utf-8'), hashlib.sha512).hexdigest()


def build_all_coin_sign(params, secret_key):
    sign = ''
    for key in sorted(params.keys()):
        sign += key + '=' + str(params[key]) + '&'
    data = sign + 'secret_key=' + secret_key
    return hashlib.md5(data.encode("utf8")).hexdigest().upper()


def http_get(url, verify=True):
    requests.packages.urllib3.disable_warnings()
    return requests.get(url, verify=verify, timeout=10).json()


def http_post(url, params, verify=True):
    headers = {
        "Content-type": "application/x-www-form-urlencoded",
    }
    temp_params = urllib.parse.urlencode(params)
    requests.packages.urllib3.disable_warnings()
    r = requests.post(url, temp_params, headers=headers, verify=verify, timeout=10)
    return r.json()


def build_bit_z_sign(params, secret_key):
    sign = ''
    for key in sorted(params.keys()):
        sign += key + '=' + str(params[key]) + '&'
    if len(sign) > 0:
        data = sign[:-1] + secret_key
    else:
        data = secret_key
    return hashlib.md5(data.encode("utf8")).hexdigest()


def extract_symbol(symbol):
    # type: (str) -> list
    return symbol.split('_')
