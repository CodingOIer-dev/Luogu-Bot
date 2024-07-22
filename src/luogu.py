import json as js
import requests


def get(url='https://www.luogu.com.cn/', headers={}, json={}):
    return requests.post(
        url='http://127.0.0.1:9000',
        timeout=60,
        json={
            'method': 'GET',
            'url': url,
            'headers': js.dumps(headers),
            'json': js.dumps(json),
        },
    )


def post(url='https://www.luogu.com.cn/', headers={}, json={}):
    return requests.post(
        url='http://127.0.0.1:9000',
        timeout=60,
        json={
            'method': 'POST',
            'url': url,
            'headers': js.dumps(headers),
            'json': js.dumps(json),
        },
    )
