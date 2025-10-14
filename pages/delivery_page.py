from locators.locators import DeliveryPageLocators
from pages.base_page import BasePage
import allure



class DeliveryPage(BasePage):

    def get_delivery_page_title(self):
        with allure.step('Проверить заголовок страницы доставки'):
            return self.get_text(DeliveryPageLocators.DELIVERY_PAGE_TITLE)
