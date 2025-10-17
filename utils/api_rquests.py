import allure


class CartService:
    def __init__(self, api_client):
        self.client = api_client


    @allure.step("Добавить товар {product_guid} в корзину (количество: {qty})")
    def add_product_to_cart(self, product_guid, qty):
        response = self.client.post(
            f"/cart/v2/products/{product_guid}?city_code=spb",
            json={"qty": qty,"services": []}
        )
        return response


    @allure.step("Получить добавленный товар в корзину")
    def get_cart_item(self, product_guid):
        response = self.client.get("/cart/v2/items?city_code=spb")

        products = response.json()['data']['products']
        for product in products:
            if product['product_guid'] == product_guid:
                return product
        return None

    @allure.step("Получить количество товаров в корзине")
    def get_count_product_in_cart(self):
        response = self.client.get("/cart/v2/items?city_code=spb")
        count = response.json()['data']['totals']['items_count']
        return count


    @allure.step("далить товар {product_guid} из корзины")
    def remove_product_from_cart(self, product_guid):
        response = self.client.delete(f"/cart/v2/products/{product_guid}?city_code=spb")
        return response


    @allure.step("Изменить количество товара {product_guid} до {qty}")
    def update_product_quantity(self, product_guid, qty):
        response = self.client.put(
            f"/cart/v2/products/{product_guid}?city_code=spb",
            json={"qty": qty,"services": []}
        )
        return response



class ProductService:
    def __init__(self, api_client):
        self.client = api_client


    @allure.step("Получить информацию о товаре по артикулу {product_code}")
    def get_product_by_code(self, product_code):
        response = self.client.get(f"/catalog/v5/products/{product_code}?city_code=spb")
        return response


    @allure.step("Получить GUID товара по артикулу {product_code}")
    def get_product_guid(self, product_code):
        product_data = self.get_product_by_code(product_code)
        return product_data['data']['product']['product_guid']


class FavoriteService:
    def __init__(self, api_client):
        self.client = api_client


    @allure.step("Добавить товар с артикулом {product_code} в избранное")
    def add_to_favorite(self, product_code):
        response = self.client.post(
            "/catalog/v5/favorites/products?city_code=spb",
            json={"code": int(product_code)}
        )
        return response


    @allure.step("Удалить товар с артикулом {product_code} из избранного")
    def remove_from_favorite(self, product_code):
        response = self.client.delete(f"/catalog/v5/favorites/products/{product_code}?city_code=spb")
        return response


class AuthService:
    def __init__(self, api_client):
        self.client = api_client


    @allure.step("Авторизоваться под пользователем {email}")
    def login(self, email, password):
        response = self.client.post(
            "/user/v1.1/login?pet_case=camel&city_code=spb&client_id=pet_site",
            json={
                "password":password,
                "email":email
                 }
        )
        return response


    @allure.step("Выйти из аккаунта")
    def logout(self):
        response = self.client.get("/user/v1.1/logout?city_code=spb")
        return response
