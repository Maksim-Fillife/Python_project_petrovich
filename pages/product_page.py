from selenium.common import StaleElementReferenceException
from locators.locators import ProductCardLocators
from pages.base_page import BasePage
import allure


class ProductPage(BasePage):
    def get_product_title(self):
        with allure.step('Проверить название товара'):
            element = self.find_element(ProductCardLocators.TITLE_IN_CART)
            return element.text

    def add_to_favourite(self):
        with allure.step('Добавить товар в избранное'):
            element = self.find_element(ProductCardLocators.ADD_TO_FAVORITE_BUTTON)
            element.click()

    def add_to_cart(self, max_retries=3):
        with allure.step('Добавить товар в корзину'):
            for i in range(max_retries):
                try:
                    self.click(ProductCardLocators.ADD_TO_CART_BUTTON)
                    break
                except StaleElementReferenceException:
                    if i == max_retries - 1:
                        raise

    def check_added_to_cart(self):
        with allure.step('Проверка добавления товара в корзину'):
            assert self.wait_for_text_in_element(ProductCardLocators.ADD_TO_CART_BUTTON, 'В корзине'), \
                "Текст кнопки не изменился на 'в корзине' после добавления"

    def get_favorite_added_message(self):
        with allure.step('Проверка добавления товара в избранное'):
            self.is_element_visible(ProductCardLocators.FAVORITE_ADDED_MESSAGE)
            return self.get_text(ProductCardLocators.FAVORITE_ADDED_MESSAGE)
