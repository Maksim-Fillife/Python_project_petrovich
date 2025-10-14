


class CartService:
    def __init__(self, api_client):
        self.client = api_client

    def add_product_to_cart(self, product_guid, qty):
        response = self.client.post(
            f"/cart/v2/products/{product_guid}?city_code=spb",
            json={"qty": qty,"services": []}
        )
        return response


    def get_cart_items(self, product_guid):
        response = self.client.get("/cart/v2/items?city_code=spb")

        products = response.json()['data']['products']
        for product in products:
            if product['product_guid'] == product_guid:
                return product
        return None

    def remove_product_from_cart(self, product_guid):
        response = self.client.delete(f"/cart/v2/products/{product_guid}?city_code=spb")
        return response

    def update_product_quantity(self, product_guid, qty):
        response = self.client.put(
            f"/cart/v2/products/{product_guid}?city_code=spb",
            json={"qty": qty,"services": []}
        )
        return response



class ProductService:
    def __init__(self, api_client):
        self.client = api_client

    def get_product_by_code(self, product_code):
        response = self.client.get(f"/catalog/v5/products/{product_code}?city_code=spb")
        return response

    def get_product_guid(self, product_code):
        product_data = self.get_product_by_code(product_code)
        return product_data['data']['product']['product_guid']


class FavoriteService:
    def __init__(self, api_client):
        self.client = api_client

    def add_to_favorite(self, product_code):
        response = self.client.post(
            "/catalog/v5/favorites/products?city_code=spb",
            json={"code": product_code}
        )
        return response

    def remove_from_favorite(self, product_code):
        response = self.client.delete(f"/catalog/v5/favorites/products/{product_code}?city_code=spb")
        return response


class AuthService:
    def __init__(self, api_client):
        self.client = api_client

    def login(self, email, password):
        response = self.client.post(
            "/user/v1.1/login?pet_case=camel&city_code=spb&client_id=pet_site",
            json={
                "password":password,
                "email":email
                 }
        )
        return response

    def logout(self):
        response = self.client.get("/user/v1.1/logout?city_code=spb")
        return response
