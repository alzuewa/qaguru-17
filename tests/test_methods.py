import requests

BASE_URL = 'https://reqres.in/api'


def is_endpoint_responsive(method: str, endpoint_url: str):
    url = BASE_URL + endpoint_url
    response = requests.request(method=method, url=url)
    return 100 <= response.status_code <= 499


def test_user_methods():
    url = '/users/1'
    assert is_endpoint_responsive('GET', url)
    assert is_endpoint_responsive('PUT', url)
    assert is_endpoint_responsive('PATCH', url)
    assert is_endpoint_responsive('DELETE', url)


def test_logout():
    url = '/logout'
    assert is_endpoint_responsive('POST', url)
