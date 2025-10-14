from pages.main_page import MainPage
from locators.locators import CartPageLocators
import allure


class CartPage(MainPage):

    def delete_product_from_cart(self):
        with allure.step('Удалить продукт из корзины'):
         self.click(CartPageLocators.DELETE_FROM_CART_BUTTON)

    def is_cart_empty(self):
        with allure.step('Проверить корзину на отсутствие товаров'):
            self.wait_for_text_in_element(CartPageLocators.EMPTY_CART_MESSAGE, 'Корзина пуста.')