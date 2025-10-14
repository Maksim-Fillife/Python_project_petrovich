from selenium.common import exceptions
from locators.locators import ProductCardLocators
from locators.locators import MainPageLocators
from pages.base_page import BasePage
from selenium.webdriver import Keys
from data.config import BASE_URL
import allure
import random


class MainPage(BasePage):

    def open(self):
        with allure.step('Open main page https://petrovich.ru/'):
            self.driver.get(BASE_URL)

    def open_login_modal(self, max_retries=3):
        with allure.step('Открыть форму авторизаации'):
            for i in range(max_retries):
                try:
                    self.click(MainPageLocators.LOGIN_BUTTON)
                    break
                except exceptions.TimeoutException:
                    if i == max_retries - 1:
                        raise


    def open_services(self):
        with allure.step('Открыть раздел "Сервисы'):
            self.click(MainPageLocators.SERVICES_ICON)

    def search_product(self, keyword):
        with allure.step(f'Ввести текст {keyword} и нажать Enter'):
            self.type_text(MainPageLocators.HEADER_SEARCH_INPUT, keyword)
            self.driver.find_element(*MainPageLocators.HEADER_SEARCH_INPUT).send_keys(Keys.ENTER)

    def check_product_exist(self, keyword):
        with allure.step('Провверить результат поиска'):
            search_result = self.get_text(MainPageLocators.SEARCH_RESULT)
            assert keyword.lower() in search_result.lower(), \
                f"Ожидаемый ключ '{keyword}' не найден в результате: '{search_result}'"

    def get_title_cards(self):
        with allure.step('Получить название карточек товаров'):
            self.find_elements(ProductCardLocators.PRODUCT_TITLE)
            return self.find_elements(ProductCardLocators.PRODUCT_TITLE)

    def select_random_product(self):
        with allure.step('Выбрать случайный товар'):
            cards = self.get_title_cards()
            assert len(cards) > 0, "Товары не найдены"
            select_product = random.choice(cards)
            product_name = select_product.text
            self.click(select_product)
            return product_name

    def open_mini_cart(self):
        with allure.step('Открыть всплывающую мини-корзину'):
            self.hover(MainPageLocators.CART_ICON)

    def open_cart(self):
        with allure.step('Открыть корзину'):
            self.click(MainPageLocators.CART_ICON)

    def get_footer_section_titles(self):
        with allure.step('Посмотреть зоголовки футера'):
            elements = self.find_elements(MainPageLocators.FOOTER_TITLE)
            return {el.text.strip() for el in elements if el.text.strip()}


