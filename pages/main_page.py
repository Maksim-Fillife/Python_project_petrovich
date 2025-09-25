import random
from data.config import BASE_URL
from selenium.webdriver import Keys
from pages.base_page import BasePage
from locators.locators import MainPageLocators
from locators.locators import ProductCardLocators


class MainPage(BasePage):

    def open(self):
        self.driver.get(BASE_URL)

    def open_login_modal(self):
        self.click(MainPageLocators.LOGIN_BUTTON)

    def search_product(self, keyword):
        self.type_text(MainPageLocators.HEADER_SEARCH_INPUT, keyword)
        self.driver.find_element(*MainPageLocators.HEADER_SEARCH_INPUT).send_keys(Keys.ENTER)

    def get_product_cards(self):
        self.find_elements(ProductCardLocators.PRODUCT_TITLE)
        return self.find_elements(ProductCardLocators.PRODUCT_TITLE)

    def select_random_product(self):
        cards = self.get_product_cards()
        assert len(cards) > 0, "Товары не найдены"
        select_product = random.choice(cards)
        product_name = select_product.text
        select_product.click()
        return product_name

