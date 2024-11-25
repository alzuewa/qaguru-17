import json
import os

import jsonschema
import pytest
from dotenv import load_dotenv

from models.schemas import authorization as schema

load_dotenv()

new_user_password = os.getenv('NEW_USER_PASSWORD')
existing_user_password = os.getenv('EXISTING_USER_PASSWORD')


class TestPositive:

    @pytest.mark.skip('Imaginary JIRA bug #123; does not work')
    def test_post_register(self, reqres_api):
        data = {
            'username': 'Test User',
            'email': 'test.user@reqres.in',
            'password': new_user_password
        }
        response = reqres_api.post(endpoint_path='/register', json=data)
        assert response.status_code == 200
        jsonschema.validate(instance=response, schema=schema.post_register)

    @pytest.mark.skip("Fake test; impossible to register, existing users passwords are unknown")
    def test_post_login(self, reqres_api):
        data = {
            'username': 'Janet Weaver',
            'email': 'janet.weaver@reqres.in',
            'password': existing_user_password
        }
        response = reqres_api.post(endpoint_path='/login', json=data)
        assert response.status_code == 200
        jsonschema.validate(instance=response, schema=schema.post_login)

    def test_post_logout(self, reqres_api):
        response = reqres_api.post(endpoint_path='/logout')
        assert response.status_code == 200
        assert response.json() == {}


class TestNegative:

    def test_post_register_missed_all_required_fields(self, reqres_api):
        data = {}
        response = reqres_api.post(endpoint_path='/register', json=data)
        assert response.status_code == 400
        json_content = json.loads(response.text)
        assert json_content.get('error') == 'Missing email or username'

    def test_post_register_missed_password(self, reqres_api):
        data = {'username': 'Test User', 'email': 'test.user@reqres.in'}
        response = reqres_api.post(endpoint_path='/register', json=data)
        assert response.status_code == 400
        json_content = json.loads(response.text)
        assert json_content.get('error') == 'Missing password'

    def test_post_register_missed_username(self, reqres_api):
        data = {'email': 'test.user@reqres.in', 'password': new_user_password}
        response = reqres_api.post(endpoint_path='/register', json=data)
        assert response.status_code == 400
        json_content = json.loads(response.text)
        assert json_content.get('error') == 'Note: Only defined users succeed registration'

    def test_post_register_missed_email(self, reqres_api):
        data = {'email': 'test.user@reqres.in', 'password': new_user_password}
        response = reqres_api.post(endpoint_path='/register', json=data)
        assert response.status_code == 400
        json_content = json.loads(response.text)
        assert json_content.get('error') == 'Note: Only defined users succeed registration'

    def test_post_login_missed_password(self, reqres_api):
        data = {'username': 'Test User', 'email': 'test.user@reqres.in'}
        response = reqres_api.post(endpoint_path='/login', json=data)
        assert response.status_code == 400
        json_content = json.loads(response.text)
        assert json_content.get('error') == 'Missing password'

    def test_post_login_missed_username_and_email(self, reqres_api):
        data = {'password': existing_user_password}
        response = reqres_api.post(endpoint_path='/login', json=data)
        assert response.status_code == 400
        json_content = json.loads(response.text)
        assert json_content.get('error') == 'Missing email or username'

    def test_post_login_username_not_exist(self, reqres_api):
        data = {'username': 'Fake User', 'password': existing_user_password}
        response = reqres_api.post(endpoint_path='/login', json=data)
        assert response.status_code == 400
        json_content = json.loads(response.text)
        assert json_content.get('error') == 'user not found'

    def test_post_login_email_not_exist(self, reqres_api):
        data = {'email': 'fake.user@reqres.in', 'password': existing_user_password}
        response = reqres_api.post(endpoint_path='/login', json=data)
        assert response.status_code == 400
        json_content = json.loads(response.text)
        assert json_content.get('error') == 'user not found'
