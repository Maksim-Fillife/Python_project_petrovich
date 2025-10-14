from locators.locators import ServicesPageLocators
from pages.base_page import BasePage
import allure


class ServicesPage(BasePage):

    def open_delivery_page(self):
        with allure.step('Открыть страницу доставки'):
            self.click(ServicesPageLocators.DELIVERY_PAGE_BUTTON)