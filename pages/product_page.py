from pages.base_page import BasePage
from locators.locators import ProductCardLocators


class ProductPage(BasePage):
    def get_product_title(self):
        element = self.find_element(ProductCardLocators.TITLE_IN_CART)
        return element.text