from data.config import COOKIES
from utils.api_client import ApiClient
import requests
import pytest
from utils.data_loader import load_random_product_code


@pytest.fixture
def api_client():

    session = requests.Session()
    session.headers.update({
        'Accept': 'application/json, text/plain, */*',
        'Accept-Language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
        'Referer': 'https://petrovich.ru/product/147312/',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.0.0 Safari/537.36'
       })
    session.headers['Cookie'] = COOKIES
    client = ApiClient(base_url="https://api.petrovich.ru", session=session)
    yield client
    session.close()

@pytest.fixture
def product_code(api_client):
    return load_random_product_code()


@pytest.fixture
def product_guid(api_client, product_code):
    endpoint = f"/catalog/v5/products/{product_code}?city_code=spb"
    result = api_client.get(endpoint)
    json_data = result.json()
    print(json_data)
    guid = json_data["data"]['product']['product_guid']
    print(guid)
    return guid



@pytest.fixture(scope='session', autouse=True)
def cleanup_favorites(api_client):
    yield
    api_client.delete('/catalog/v5/favorites/products?city_code=spb')

@pytest.fixture(scope='session', autouse=True)
def logout_after_tests(api_client):
    api_client.post('/user/v1.1/logout?city_code=spb')

