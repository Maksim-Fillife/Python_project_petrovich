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

    def open_login_modal(self):
        with allure.step('Open authorization form'):
            self.click(MainPageLocators.LOGIN_BUTTON)

    def open_services(self):
        with allure.step('Оpen the services section'):
            self.click(MainPageLocators.SERVICES_ICON)

    def search_product(self, keyword):
        with allure.step('Enter text and click find'):
            self.type_text(MainPageLocators.HEADER_SEARCH_INPUT, keyword)
            self.driver.find_element(*MainPageLocators.HEADER_SEARCH_INPUT).send_keys(Keys.ENTER)

    def check_product_exist(self, keyword):
        with allure.step('Check if product exist'):
            search_result = self.get_text(MainPageLocators.SEARCH_RESULT)
            assert keyword.lower() in search_result.lower(), \
                f"Ожидаемый ключ '{keyword}' не найден в результате: '{search_result}'"

    def get_title_cards(self):
        with allure.step('get_title_cards'):
            self.find_elements(ProductCardLocators.PRODUCT_TITLE)
            return self.find_elements(ProductCardLocators.PRODUCT_TITLE)

    def select_random_product(self):
        with allure.step('Select random product'):
            cards = self.get_title_cards()
            assert len(cards) > 0, "Товары не найдены"
            select_product = random.choice(cards)
            product_name = select_product.text
            select_product.click()
            return product_name

    def open_mini_cart(self):
        with allure.step('Open mini cart'):
            self.hover(MainPageLocators.CART_ICON)

    def open_cart(self):
        with allure.step('Open cart'):
            self.click(MainPageLocators.CART_ICON)

    def get_footer_section_titles(self):
        with allure.step('Get footer section titles'):
            elements = self.find_elements(MainPageLocators.FOOTER_TITLE)
            return {el.text.strip() for el in elements if el.text.strip()}


