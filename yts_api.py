
import requests


def make_request(url="http://yts.re/api/list.json", **params):
    return requests.get(url, params=params).json()


def search(**params):
    results = make_request(**params)
    if 'error' in results.keys():
        return results['error']
    return results["MovieList"]

