from typing import Optional

import requests

URL = 'https://reqres.in/api/users'


def get_response_code(method: str, endpoint_url: Optional[str] = None, **kwargs):
    url = f'{URL}{endpoint_url}'
    response = requests.request(method=method, url=url, **kwargs)
    return response.status_code


def test_get_users_returns_200():
    assert get_response_code('GET') == 200


def test_delete_users_returns_204():
    assert get_response_code('DELETE') == 204


def test_create_user_returns_201():
    body = {'name': 'testuser', 'email': 'testuser@example.com'}
    assert get_response_code('POST', json=body) == 201


def test_get_users_with_id_returns_404():
    assert get_response_code('GET', endpoint_url='/100') == 404


def test_register_returns_400():
    user_data = {
        'username': 'testuser',
        'email': 'testuser@example.com',
        'password': '12345'
    }
    response = requests.post(
        url='https://reqres.in/api/register',
        json=user_data
    )
    assert response.status_code == 400
