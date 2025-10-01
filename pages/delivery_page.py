from locators.locators import DeliveryPageLocators
from pages.base_page import BasePage
import allure



class DeliveryPage(BasePage):

    def check_delivery_page_title(self):
        with allure.step('check delivery page title'):
            title_text = self.get_text(DeliveryPageLocators.DELIVERY_PAGE_TITLE)
            assert "Доставка и подъем" in title_text, \
                "Ожидался текст 'Доставка и подъем'"