from utils.data_loader import load_all_product_code
from jsonschema import validate
from pathlib import Path
import pytest
import json
from utils.api_rquests import ProductService, CartService, FavoriteService, AuthService
from data.config import PASSWORD, EMAIL, INVALID_PASSWORD

SCHEMA_DIR = Path(__file__).parent.parent.parent / "schemas"


@pytest.mark.parametrize("product_code", load_all_product_code())
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



def test_add_product_to_cart(api_client, product_guid):
    cart_service = CartService(api_client)
    response = cart_service.add_product_to_cart(product_guid, qty=1)

    assert response.status_code == 200

    assert response.json()['state']['title'] == 'Запрос успешно выполнен'
    check_item_in_cart = cart_service.get_cart_items(product_guid)
    assert check_item_in_cart['product_guid'] == product_guid



def test_delete_product_from_cart(api_client, product_guid):
    cart_service = CartService(api_client)
    cart_service.add_product_to_cart(product_guid, qty=1)

    response = cart_service.remove_product_from_cart(product_guid)
    assert response.status_code == 200
    items_in_cart = cart_service.get_cart_items(product_guid)
    assert not items_in_cart



def test_change_count_product_in_cart(api_client, product_guid):
    cart_service = CartService(api_client)

    cart_service.add_product_to_cart(product_guid, qty=1)

    new_quantity = 30
    response = cart_service.update_product_quantity(product_guid, new_quantity)

    assert response.status_code == 200
    cart_items = cart_service.get_cart_items(product_guid)
    assert cart_items['qty'] == new_quantity



def test_add_product_to_favorite(api_client, product_code):
    favorite_service = FavoriteService(api_client)

    response = favorite_service.add_to_favorite(product_code)

    assert response.status_code == 200
    assert response.json()['state']['title'] == 'ОК'



def test_auth_success(api_client):
    auth_service = AuthService(api_client)

    response = auth_service.login(email=EMAIL, password=PASSWORD)
    assert response.status_code == 200
    assert response.json()['state']['title'] == 'Пользователь авторизован'



def test_authorization_with_invalid_password(api_client):
    auth_service = AuthService(api_client)

    response = auth_service.login(email=EMAIL, password=INVALID_PASSWORD)
    assert response.status_code == 400
    assert response.json()['errors'][0]['title'] == 'Неверный пароль'