import requests
from requests import Session


class ApiSession(Session):

    def __init__(self, base_url):
        super().__init__()
        self.base_url = base_url

    def request(self, endpoint_path: str, method: str, **kwargs) -> requests.Response:
        url = f'{self.base_url}{endpoint_path}'
        return super().request(url=url, method=method, **kwargs)

    def get(self, endpoint_path: str, **kwargs) -> requests.Response:
        return self.request(endpoint_path, method='GET', **kwargs)

    def post(self, endpoint_path: str, **kwargs) -> requests.Response:
        return self.request(endpoint_path, method='POST', **kwargs)

    def put(self, endpoint_path: str, **kwargs) -> requests.Response:
        return self.request(endpoint_path, method='PUT', **kwargs)

    def patch(self, endpoint_path: str, **kwargs) -> requests.Response:
        return self.request(endpoint_path, method='PATCH', **kwargs)

    def delete(self, endpoint_path: str, **kwargs) -> requests.Response:
        return self.request(endpoint_path, method='DELETE', **kwargs)
