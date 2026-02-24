import pytest

from utils.api_client import ApiClient


@pytest.fixture(scope="session")
def base_url():
    return "https://petstore.swagger.io/v2"


@pytest.fixture(scope="session")
def api(base_url):
    return ApiClient(base_url)
