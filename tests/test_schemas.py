import jsonschema
import requests

import models.schemas.resources as schemas

BASE_URL = 'https://reqres.in/api/resources'
TEST_RESOURCE_URL = f'{BASE_URL}/1'


def test_get_resources():
    response = requests.get(url=BASE_URL)
    jsonschema.validate(instance=response.json(), schema=schemas.get_resources)


def test_get_resource():
    response = requests.get(url=TEST_RESOURCE_URL)
    jsonschema.validate(instance=response.json(), schema=schemas.get_resource)


def test_put_resource():
    response = requests.put(url=TEST_RESOURCE_URL)
    jsonschema.validate(instance=response.json(), schema=schemas.put_resource)


def test_patch_resource():
    response = requests.patch(url=TEST_RESOURCE_URL)
    jsonschema.validate(instance=response.json(), schema=schemas.patch_resource)


def test_delete_resource():
    response = requests.delete(url=TEST_RESOURCE_URL)
    assert not response.text
    assert response.reason == 'No Content'
