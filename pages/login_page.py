from data.config import PASSWORD, EMAIL, INVALID_PASSWORD
from locators.locators import LoginPageLocators
from pages.base_page import BasePage



class LoginPage(BasePage):

    def fill_email(self):
        self.type_text(LoginPageLocators.EMAIL_INPUT, EMAIL)

    def fill_password(self):
        self.type_text(LoginPageLocators.PASSWORD_INPUT, PASSWORD)

    def fill_invalid_password(self):
        self.type_text(LoginPageLocators.PASSWORD_INPUT, INVALID_PASSWORD)

    def submit_authorization(self):
        self.click(LoginPageLocators.ENTER_BUTTON)

    def check_successful_auth(self):
        self.hover(LoginPageLocators.PROFILE_BUTTON)
        return self.is_element_visible(LoginPageLocators.PROFILE_POPUP)

    def open_profile_popup(self):
        self.hover(LoginPageLocators.PROFILE_BUTTON)

    def click_logout(self):
        self.click(LoginPageLocators.LOGOUT_BUTTON)

    def check_unsuccessful_auth(self):
        self.hover(LoginPageLocators.PROFILE_BUTTON)