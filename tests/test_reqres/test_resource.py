import datetime
from datetime import datetime

import jsonschema
import pytest

import models.schemas.resources as schemas


class TestGetAllResources:

    def test_without_params(self, reqres_api):
        response = reqres_api.get(endpoint_path='/resource')
        resp_json = response.json()
        resources_per_page = len(resp_json.get('data'))

        assert response.status_code == 200
        jsonschema.validate(instance=response.json(), schema=schemas.get_resources)
        assert resp_json.get('page') == 1
        assert resp_json.get('per_page') == resources_per_page
        assert resp_json.get('total') == 12
        assert resp_json.get('total_pages') == resp_json.get('total') / resources_per_page
        assert len(resp_json.get('data')) == resources_per_page

    def test_with_default_params(self, reqres_api):
        params = {'page': 1, 'per_page': 6}

        response = reqres_api.get(endpoint_path='/resource', params=params)
        resp_json = response.json()
        resources_per_page = params['per_page']

        assert response.status_code == 200
        jsonschema.validate(instance=response.json(), schema=schemas.get_resources)
        assert resp_json.get('page') == params['page']
        assert resp_json.get('per_page') == resources_per_page
        assert resp_json.get('total') == 12
        assert resp_json.get('total_pages') == resp_json.get('total') / resources_per_page
        assert len(resp_json.get('data')) == resources_per_page

    def test_with_non_default_params(self, reqres_api):
        params = {'page': 2, 'per_page': 3}

        response = reqres_api.get(endpoint_path='/resource', params=params)
        resp_json = response.json()
        resources_per_page = params['per_page']

        assert response.status_code == 200
        jsonschema.validate(instance=response.json(), schema=schemas.get_resources)
        assert resp_json.get('page') == params['page']
        assert resp_json.get('per_page') == resources_per_page
        assert resp_json.get('total') == 12
        assert resp_json.get('total_pages') == resp_json.get('total') / resources_per_page
        assert len(resp_json.get('data')) == resources_per_page

    def test_with_page_param(self, reqres_api):
        params = {'page': 2}

        response = reqres_api.get(endpoint_path='/resource', params=params)
        resp_json = response.json()

        assert response.status_code == 200
        jsonschema.validate(instance=response.json(), schema=schemas.get_resources)
        assert resp_json.get('page') == params['page']
        assert resp_json.get('per_page') == 6
        assert resp_json.get('total') == 12
        assert resp_json.get('total_pages') == resp_json.get('total') / resp_json.get('per_page')
        assert len(resp_json.get('data')) == resp_json.get('per_page')

    def test_with_per_page_param(self, reqres_api):
        params = {'per_page': 4}

        response = reqres_api.get(endpoint_path='/resource', params=params)
        resp_json = response.json()
        resources_per_page = params['per_page']

        assert response.status_code == 200
        jsonschema.validate(instance=response.json(), schema=schemas.get_resources)
        assert resp_json.get('page') == 1
        assert resp_json.get('per_page') == resources_per_page
        assert resp_json.get('total') == 12
        assert resp_json.get('total_pages') == resp_json.get('total') / resources_per_page
        assert len(resp_json.get('data')) == resources_per_page

    def test_inexistent_page(self, reqres_api):
        params = {'page': 100}

        response = reqres_api.get(endpoint_path='/resource', params=params)
        resp_json = response.json()

        assert response.status_code == 200
        jsonschema.validate(instance=response.json(), schema=schemas.get_resources)
        assert resp_json.get('page') == params['page']
        assert resp_json.get('per_page') == 6
        assert resp_json.get('total') == 12
        assert resp_json.get('total_pages') == 2
        assert len(resp_json.get('data')) == 0

    def test_exceeded_per_page_value(self, reqres_api):
        params = {'per_page': 100}

        response = reqres_api.get(endpoint_path='/resource', params=params)
        resp_json = response.json()

        assert response.status_code == 200
        jsonschema.validate(instance=response.json(), schema=schemas.get_resources)
        assert resp_json.get('page') == 1
        assert resp_json.get('per_page') == params['per_page']
        assert resp_json.get('total') == 12
        assert resp_json.get('total_pages') == 1
        assert len(resp_json.get('data')) == resp_json.get('total')

    @pytest.mark.parametrize('page', [1, 2, 800])
    def test_ads_always_present_in_response(self, reqres_api, page):
        params = {'page': page}

        response = reqres_api.get(endpoint_path='/resource', params=params).json()
        ads_info = response.get('support')

        assert len(ads_info) == 2
        assert all(key in ads_info for key in ('url', 'text'))
        assert 'https://contentcaddy.io' in ads_info['url']
        assert 'Content Caddy' in ads_info['text']


class TestGetResource:

    def test_existing_resource(self, reqres_api):
        response = reqres_api.get(endpoint_path='/resource/1')
        resp_json = response.json()['data']

        assert response.status_code == 200
        jsonschema.validate(instance=response.json(), schema=schemas.get_resource)
        assert resp_json.get('id') == 1
        assert resp_json.get('name') == 'cerulean'
        assert resp_json.get('year') == 2000
        assert resp_json.get('color') == '#98B2D1'
        assert resp_json.get('pantone_value') == '15-4020'

    def test_non_existent_resource(self, reqres_api):
        response = reqres_api.get(endpoint_path='/resource/13')

        assert response.status_code == 404
        jsonschema.validate(instance=response.json(), schema=schemas.get_invalid_resourse)


class TestPostResource:

    def test_send_one_field(self, reqres_api):
        data = {'name': 'any'}
        response = reqres_api.post(endpoint_path='/resource', json=data)
        resp_json = response.json()

        assert response.status_code == 201
        assert resp_json.get('name') == data['name']
        jsonschema.validate(instance=resp_json, schema=schemas.post_resource)

    def test_send_several_fields(self, reqres_api):
        data = {'name': 'any', 'color': 'green', 'size': 'medium'}
        response = reqres_api.post(endpoint_path='/resource', json=data)
        resp_json = response.json()

        assert response.status_code == 201
        for key, value in data.items():
            assert resp_json.get(key) == value
        jsonschema.validate(instance=resp_json, schema=schemas.post_resource)


class TestPutResource:

    def test_update_without_body(self, reqres_api):
        current_date = datetime.today().date()

        response = reqres_api.put(endpoint_path='/resource/1')
        resp_json = response.json()
        date_from_response = datetime.fromisoformat(resp_json['updatedAt']).date()

        assert response.status_code == 200
        jsonschema.validate(instance=resp_json, schema=schemas.put_resource)
        assert date_from_response == current_date

    def test_update_with_body(self, reqres_api):
        data = {'first_name': 'Any F', 'last_name': 'Any L'}
        current_date = datetime.today().date()

        response = reqres_api.put(endpoint_path='/resource/1', json=data)
        resp_json = response.json()
        date_from_response = datetime.fromisoformat(resp_json['updatedAt']).date()

        assert response.status_code == 200
        jsonschema.validate(instance=resp_json, schema=schemas.put_resource)
        assert date_from_response == current_date
        assert resp_json.get('first_name') == 'Any F'
        assert resp_json.get('last_name') == 'Any L'


class TestPatchResource:

    def test_patch_without_body(self, reqres_api):
        current_date = datetime.today().date()

        response = reqres_api.patch(endpoint_path='/resource/1')
        resp_json = response.json()
        date_from_response = datetime.fromisoformat(resp_json['updatedAt']).date()

        assert response.status_code == 200
        jsonschema.validate(instance=resp_json, schema=schemas.patch_resource)
        assert date_from_response == current_date

    def test_patch_with_body(self, reqres_api):
        data = {'last_name': 'Patched'}
        current_date = datetime.today().date()

        response = reqres_api.patch(endpoint_path='/resource/1', json=data)
        resp_json = response.json()
        date_from_response = datetime.fromisoformat(resp_json['updatedAt']).date()

        assert response.status_code == 200
        jsonschema.validate(instance=resp_json, schema=schemas.patch_resource)
        assert date_from_response == current_date
        assert resp_json.get('last_name') == 'Patched'


class TestDeleteResource:

    def test_delete_resource(self, reqres_api):
        response = reqres_api.delete(endpoint_path='/resource/1')
        assert response.status_code == 204
        assert not response.text
