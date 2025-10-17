from typing import Callable, Any

from utils.data_loader import load_all_product_code
from jsonschema import validate
from pathlib import Path
import pytest
import json
from utils.api_rquests import ProductService, CartService, FavoriteService, AuthService
from data.config import PASSWORD, EMAIL, INVALID_PASSWORD
import allure
from allure_commons.types import Severity

SCHEMA_DIR = Path(__file__).parent.parent.parent / "schemas"


@pytest.mark.parametrize("product_code", load_all_product_code())
@allure.severity(Severity.NORMAL)
@allure.label('owner', 'Maksim-Fillife')
@allure.feature("Каталог товаров")
@allure.story("Получение товара по артикулу")
@allure.title("Получение товара по коду: {product_code}")
@pytest.mark.api
def test_get_product_by_code(api_client, product_code):
    product_service = ProductService(api_client)
    response = product_service.get_product_by_code(product_code)

    assert response.status_code == 200

    json_data = response.json()
    code = json_data["data"]['product']

    schema_path = SCHEMA_DIR / "search_product.json"
    with open(schema_path, encoding='utf8') as file:
        schema = json.load(file)
    validate(instance=json_data, schema=schema)
    assert str(code["code"]) == product_code



@allure.severity(Severity.CRITICAL)
@allure.label('owner', 'Maksim-Fillife')
@allure.feature("Корзина")
@allure.story("Добавление товара в корзину")
@allure.title("Успешное добавление товара в корзину")
@pytest.mark.api
def test_add_product_to_cart(api_client, product_guid):
    cart_service = CartService(api_client)
    response = cart_service.add_product_to_cart(product_guid, qty=1)

    assert response.status_code == 200

    assert response.json()['state']['title'] == 'Запрос успешно выполнен'
    check_item_in_cart = cart_service.get_cart_item(product_guid)
    assert check_item_in_cart['product_guid'] == product_guid



@allure.severity(Severity.CRITICAL)
@allure.label('owner', 'Maksim-Fillife')
@allure.feature("Корзина")
@allure.story("Удаление товара из корзины")
@allure.title("Удаление товара из корзины")
@pytest.mark.api
def test_delete_product_from_cart(api_client, product_guid):
    cart_service = CartService(api_client)
    cart_service.add_product_to_cart(product_guid, qty=1)

    response = cart_service.remove_product_from_cart(product_guid)
    assert response.status_code == 200
    item_in_cart = cart_service.get_cart_item(product_guid)
    assert not item_in_cart



@allure.severity(Severity.NORMAL)
@allure.label('owner', 'Maksim-Fillife')
@allure.feature("Корзина")
@allure.story("Изменение количества товара")
@allure.title("Изменение количества товара в корзине")
@pytest.mark.api
def test_change_count_product_in_cart(api_client, product_guid):
    cart_service = CartService(api_client)

    cart_service.add_product_to_cart(product_guid, qty=1)
    in_cart = cart_service.get_count_product_in_cart()
    assert in_cart > 0

    new_quantity = 30
    response = cart_service.update_product_quantity(product_guid, new_quantity)

    assert response.status_code == 200
    cart_item = cart_service.get_cart_item(product_guid)
    assert cart_item['qty'] == new_quantity



@allure.severity(Severity.NORMAL)
@allure.label('owner', 'Maksim-Fillife')
@allure.feature("Избранное")
@allure.story("Добавление товара в избранное")
@allure.title("Добавление товара в избранное по артикулу")
@pytest.mark.api
def test_add_product_to_favorite(api_client, product_code):
    favorite_service = FavoriteService(api_client)

    response = favorite_service.add_to_favorite(product_code)

    assert response.status_code == 200
    assert response.json()['state']['title'] == 'ОК'



@allure.severity(Severity.CRITICAL)
@allure.label('owner', 'Maksim-Fillife')
@allure.feature("Авторизация")
@allure.story("Успешный вход в аккаунт")
@allure.title("Успешная авторизация с корректными данными")
@pytest.mark.api
def test_auth_success(api_client, logout_after_tests):
    auth_service = AuthService(api_client)

    response = auth_service.login(email=EMAIL, password=PASSWORD)
    assert response.status_code == 200
    assert response.json()['state']['title'] == 'Пользователь авторизован'



@allure.severity(Severity.NORMAL)
@allure.label('owner', 'Maksim-Fillife')
@allure.feature("Авторизация")
@allure.story("Неверный пароль")
@allure.title("Авторизация с неверным паролем")
@pytest.mark.api
def test_authorization_with_invalid_password(api_client):
    auth_service = AuthService(api_client)

    response = auth_service.login(email=EMAIL, password=INVALID_PASSWORD)

    print("Status code:", response.status_code)
    print("Response body:", response.text)

    assert response.status_code == 400
    assert response.json()['errors'][0]['title'] == 'Неверный пароль'