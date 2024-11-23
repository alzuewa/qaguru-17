import random
from unittest import mock

import pytest
import requests
from requests import Session
from requests.models import Response

URL = 'https://reqres.in/api/resources'


def test_get_without_params():
    response = requests.get(URL)

    assert response.status_code == 200
    assert len(response.json()) == 6
    assert len(response.json()['data'])


@pytest.mark.parametrize('param, value', [('page', 2), ('per_page', 3)])
def test_get_with_1_param(param, value):
    params = {param: value}

    response = requests.get(URL, params=params)

    assert response.status_code == 200
    assert len(response.json()) == 6
    assert len(response.json()['data'])


def test_get_with_all_params():
    params = {
        'page': 2,
        'per_page': 3
    }

    response = requests.get(URL, params=params)

    assert response.status_code == 200
    assert len(response.json()) == 6
    assert len(response.json()['data'])


def test_response_with_default_params_implicit():
    response = requests.get(URL).json()

    assert response['page'] == 1
    assert response['per_page'] == 6
    assert response['total'] == 12
    assert response['total_pages'] == 2
    assert len(response['data']) == response['per_page']


def test_response_with_default_params_explicit():
    params = {'page': 1, 'per_page': 6}
    response = requests.get(URL, params=params).json()

    assert response['page'] == 1
    assert response['per_page'] == 6
    assert response['total'] == 12
    assert response['total_pages'] == 2
    assert len(response['data']) == response['per_page']


def test_request_inexistent_page():
    session = Session()
    response = session.get(URL).json()
    total_pages = response['total_pages']
    requested_page = random.randint(total_pages, 1000)
    params = {'page': requested_page}

    response = session.get(URL, params=params).json()

    assert response['page'] == requested_page
    assert not len(response['data'])


@pytest.mark.parametrize('per_page', [1, 12])
def test_items_per_page_reflects_param(per_page):
    session = Session()
    params = {'per_page': per_page}

    response = session.get(URL, params=params).json()

    assert len(response['data']) == per_page


def test_request_exceeded_per_page_value():
    session = Session()
    response = session.get(URL).json()
    total_resources = response['total']
    requested_per_page = random.randint(total_resources, 1000)
    params = {'per_page': requested_per_page}

    response = session.get(URL, params=params).json()

    assert response['per_page'] == requested_per_page
    assert len(response['data']) == total_resources


@pytest.mark.parametrize('page', [1, 2, 800])
def test_ads_always_present(page):
    session = Session()
    params = {'page': page}

    response = session.get(URL, params=params).json()

    assert len(response['support'])
    assert all(key in response['support'] for key in ('url', 'text'))
    assert 'https://contentcaddy.io' in response['support']['url']
    assert 'Content Caddy' in response['support']['text']


def mocked_response(*args, **kwargs):
    response = Response()
    response.status_code = 400
    return response


@mock.patch('requests.get', side_effect=mocked_response)
def test_with_imaginary_invalid_params(mock_obj):
    params = {
        'any_param': 'any_value'
    }
    response = requests.get(URL, params=params)
    assert response.status_code == 400
