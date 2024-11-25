import pytest

from api_utils.constants import BASE_REQRES_URL
from api_utils.session import ApiSession


@pytest.fixture(scope='package')
def reqres_api() -> ApiSession:
    session = ApiSession(base_url=BASE_REQRES_URL)
    return session
